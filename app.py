import json
import random
import re
import threading
import time
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError

import schedule
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

# === Configuration ===
KANDILLI_URL = "http://www.koeri.boun.edu.tr/scripts/sondepremler.asp"
AFAD_URL = "https://deprem.afad.gov.tr/last-earthquakes.html"
REQUEST_TIMEOUT = 15  # seconds
UPDATE_INTERVAL_MINUTES = 5
API_VERSION = "1.0.0"
USER_AGENT = "MdaedalusEarthquakeAPI/1.0 (+https://github.com/mdaedalus)"

# === Global Data Buffers (thread-safe swap) ===
_data_lock = threading.Lock()
_buffers = {
    "kandilli": [],
    "afad": [],
    "last_updated": None,
    "errors": {"kandilli": None, "afad": None},
}


# === Helpers ===
def _safe_float(value, default=0.0):
    """Convert a string to float, returning default on failure."""
    try:
        value = str(value).strip()
        if value in ("", "-.-", "N/A", "null"):
            return default
        return float(value)
    except (ValueError, TypeError):
        return default


def _parse_iso_or_turkish(date_str, time_str, fmt):
    """Parse a datetime string into a UTC unix timestamp."""
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", fmt)
        # Turkish sources report local time (Europe/Istanbul, UTC+3)
        return int(dt.replace(tzinfo=timezone.utc).timestamp()) - 3 * 3600
    except (ValueError, TypeError):
        return int(datetime.now(timezone.utc).timestamp())


def _fetch_html(url):
    """Fetch HTML with a proper User-Agent and timeout."""
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        return resp.read()


# === Kandilli Observatory Scraper ===
def fetch_kandilli():
    """Fetch and parse earthquake data from Kandilli Observatory."""
    results = []
    raw_data = _fetch_html(KANDILLI_URL)
    soup = BeautifulSoup(raw_data, "html.parser")

    pre_blocks = soup.find_all("pre")
    if not pre_blocks:
        return results

    raw_text = str(pre_blocks).strip().split("--------------")
    if len(raw_text) < 3:
        return results

    records = [r.strip() for r in raw_text[2].split("\n") if r.strip()]
    if len(records) < 3:
        return results
    records = records[1:-2]

    for line in records:
        line = re.sub(r"\s+", " ", line)
        parts = line.split(" ")
        if len(parts) < 9:
            continue

        try:
            date_str, time_str = parts[0], parts[1]
            lat = _safe_float(parts[2])
            lon = _safe_float(parts[3])
            depth = _safe_float(parts[4])
            md = _safe_float(parts[5])
            ml = _safe_float(parts[6])
            mw = _safe_float(parts[7])

            # Location is everything between the depth and the status keyword
            rest = " ".join(parts[8:])
            location = re.split(r"\s+(İlksel|REVIZE|Önsel|Otomatik)\b", rest)[0].strip()
            status_match = re.search(r"(İlksel|REVIZE|Önsel|Otomatik)", rest)
            status = status_match.group(1) if status_match else "Unknown"

            timestamp = _parse_iso_or_turkish(date_str, time_str, "%Y.%m.%d %H:%M:%S")

            feature = {
                "type": "Feature",
                "properties": {
                    "mag": {"md": md, "ml": ml, "mw": mw},
                    "place": location,
                    "time": timestamp,
                    "updated": timestamp,
                    "status": status,
                    "type": "earthquake",
                    "title": f"M {ml:.1f} - {location}",
                    "depth": depth,
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat, depth],
                },
                "id": f"kandilli-{timestamp}-{random.randint(0, 999999)}",
                "source": "kandilli",
            }
            results.append(feature)
        except (IndexError, ValueError):
            continue

    return results


# === AFAD Scraper ===
def fetch_afad():
    """Fetch and parse earthquake data from AFAD."""
    results = []
    raw_data = _fetch_html(AFAD_URL)
    soup = BeautifulSoup(raw_data, "html.parser")
    rows = soup.find_all("tr")[1:]

    for row in rows:
        columns = row.find_all("td")
        if len(columns) < 7:
            continue

        try:
            date_str = columns[0].text.strip()
            lat = _safe_float(columns[1].text)
            lon = _safe_float(columns[2].text)
            depth = _safe_float(columns[3].text)
            eq_type = columns[4].text.strip().upper()
            magnitude = _safe_float(columns[5].text)
            location = columns[6].text.strip()

            timestamp = _parse_iso_or_turkish(date_str, "00:00:00", "%Y-%m-%d %H:%M:%S")
            # AFAD datetime includes time in the first column
            try:
                timestamp = int(
                    datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    .replace(tzinfo=timezone.utc)
                    .timestamp()
                ) - 3 * 3600
            except ValueError:
                pass

            feature = {
                "type": "Feature",
                "properties": {
                    "mag": {
                        "md": magnitude if eq_type == "MD" else 0,
                        "ml": magnitude if eq_type == "ML" else 0,
                        "mw": magnitude if eq_type == "MW" else 0,
                    },
                    "place": location,
                    "time": timestamp,
                    "updated": timestamp,
                    "status": eq_type,
                    "type": "earthquake",
                    "title": f"M {magnitude:.1f} - {location}",
                    "depth": depth,
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat, depth],
                },
                "id": f"afad-{timestamp}-{random.randint(0, 999999)}",
                "source": "afad",
            }
            results.append(feature)
        except (IndexError, ValueError):
            continue

    return results


# === Filtering ===
def _get_magnitude(feature):
    """Extract the largest available magnitude from a feature."""
    mag = feature["properties"]["mag"]
    return max(mag.get("ml", 0), mag.get("mw", 0), mag.get("md", 0))


def filter_by_location(location, data):
    location = location.upper()
    return [item for item in data if location in item["properties"]["place"].upper()]


def filter_by_magnitude(size, data):
    try:
        size = float(size)
    except (ValueError, TypeError):
        return data
    return [item for item in data if _get_magnitude(item) >= size]


def filter_by_magnitude_and_location(size, location, data):
    return filter_by_magnitude(size, filter_by_location(location, data))


# === Data Refresh ===
def update_data():
    """Refresh AFAD and Kandilli data. Failures are isolated per source."""
    new_kandilli = _buffers["kandilli"]
    new_afad = _buffers["afad"]
    errors = {"kandilli": None, "afad": None}

    try:
        new_kandilli = fetch_kandilli()
    except (URLError, OSError, ValueError) as exc:
        errors["kandilli"] = str(exc)

    try:
        new_afad = fetch_afad()
    except (URLError, OSError, ValueError) as exc:
        errors["afad"] = str(exc)

    with _data_lock:
        if not errors["kandilli"]:
            _buffers["kandilli"] = new_kandilli
        if not errors["afad"]:
            _buffers["afad"] = new_afad
        _buffers["errors"] = errors
        _buffers["last_updated"] = datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )


# === Scheduler Thread ===
def _scheduler_loop():
    update_data()
    schedule.every(UPDATE_INTERVAL_MINUTES).minutes.do(update_data)
    while True:
        schedule.run_pending()
        time.sleep(1)


threading.Thread(target=_scheduler_loop, daemon=True).start()


# === Flask App ===
app = Flask(__name__)


@app.route("/")
def index():
    """Root endpoint with optional query filters."""
    source_type = request.args.get("type", "kandilli").lower()
    if source_type not in ("kandilli", "afad"):
        source_type = "kandilli"

    location = request.args.get("location")
    size = request.args.get("size")

    with _data_lock:
        data = list(_buffers[source_type])
        last_updated = _buffers["last_updated"]
        errors = dict(_buffers["errors"])

    if location and size:
        data = filter_by_magnitude_and_location(size, location, data)
    elif location:
        data = filter_by_location(location, data)
    elif size:
        data = filter_by_magnitude(size, data)

    payload = {
        "type": "FeatureCollection",
        "metadata": {
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "last_updated": last_updated,
            "title": "Mdaedalus Earthquake API",
            "api_version": API_VERSION,
            "source": source_type,
            "count": len(data),
            "errors": {k: v for k, v in errors.items() if v},
        },
        "features": data,
    }

    response = jsonify(payload)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Cache-Control"] = "public, max-age=60"
    return response


@app.route("/health")
def health():
    """Liveness + freshness check."""
    with _data_lock:
        return jsonify(
            {
                "status": "ok",
                "last_updated": _buffers["last_updated"],
                "kandilli_count": len(_buffers["kandilli"]),
                "afad_count": len(_buffers["afad"]),
                "errors": {k: v for k, v in _buffers["errors"].items() if v},
            }
        )


@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "not_found", "message": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(_):
    return jsonify({"error": "internal_error", "message": "Server error"}), 500


if __name__ == "__main__":
    print(f"[INFO] Starting Mdaedalus Earthquake API v{API_VERSION}...")
    app.run(host="0.0.0.0", port=5000, debug=False)
