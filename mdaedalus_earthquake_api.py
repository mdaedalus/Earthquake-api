import re
import json
import time
import threading
import schedule
from urllib.request import urlopen
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from flask import Flask, make_response, request
import random

# === Global Data Buffers ===
afad_data = []
kandilli_data = []

# === Kandilli Observatory Scraper ===
def fetch_kandilli():
    """Fetch and parse earthquake data from Kandilli Observatory."""
    results = []
    raw_data = urlopen('http://www.koeri.boun.edu.tr/scripts/sondepremler.asp').read()
    soup = BeautifulSoup(raw_data, 'html.parser')
    raw_text = str(soup.find_all('pre')).strip().split('--------------')[2]

    records = raw_text.split('\n')
    records = [r.strip() for r in records if r.strip()][1:-2]
    unique_id = random.random()

    for line in records:
        line = re.sub(r'\s+', ' ', line)
        parts = line.split(' ')
        if len(parts) < 9:
            continue
        location = parts[8] + line.split(parts[8])[len(line.split(parts[8])) - 1].split('İlksel')[0].split('REVIZE')[0]

        feature = {
            "features": {
                "type": "Feature",
                "properties": {
                    "mag": {
                        "md": float(parts[5].replace('-.-', '0')),
                        "ml": float(parts[6].replace('-.-', '0')),
                        "mw": float(parts[7].replace('-.-', '0'))
                    },
                    "place": (float(parts[4]), location.strip()),
                    "time": int(datetime.strptime(parts[0] + " " + parts[1], "%Y.%m.%d %H:%M:%S").timestamp()),
                    "updated": int(datetime.strptime(parts[0] + " " + parts[1], "%Y.%m.%d %H:%M:%S").timestamp()),
                    "status": line.split(location)[1].split()[0],
                    "type": "earthquake",
                    "title": (float(parts[4]), location.strip())
                },
                "geometry": line.split(location)[1].split()[0],
                "coordinates": (float(parts[2]), float(parts[3]), float(parts[4])),
                "id": unique_id
            }
        }
        results.append(feature)
    return results


# === AFAD Scraper ===
def fetch_afad():
    """Fetch and parse earthquake data from AFAD."""
    results = []
    raw_data = urlopen('https://deprem.afad.gov.tr/last-earthquakes.html').read()
    soup = BeautifulSoup(raw_data, 'html.parser')
    rows = soup.find_all('tr')[1:]
    unique_id = random.random()

    for row in rows:
        columns = row.find_all('td')
        if len(columns) < 7:
            continue
        eq_type = columns[4].text
        magnitude = float(columns[5].text)
        feature = {
            "properties": {
                "mag": {
                    "md": magnitude if eq_type == "MD" else 0,
                    "ml": magnitude if eq_type == "ML" else 0,
                    "mw": magnitude if eq_type == "MW" else 0
                },
                "place": (float(columns[3].text), columns[6].text),
                "time": int(datetime.strptime(columns[0].text, "%Y-%m-%d %H:%M:%S").timestamp()),
                "updated": int(datetime.strptime(columns[0].text, "%Y-%m-%d %H:%M:%S").timestamp()),
                "status": eq_type,
                "type": "earthquake",
                "title": (float(columns[3].text), columns[6].text)
            },
            "geometry": eq_type,
            "coordinates": (float(columns[1].text), float(columns[2].text), float(columns[3].text)),
            "id": unique_id
        }
        results.append(feature)
    return results


# === Filtering Functions ===
def filter_by_location(location, data):
    return [item for item in data if location.upper() in json.dumps(item).upper()]


def filter_by_magnitude(size, data):
    return [item for item in data if float(size) <= float(item["features"]["properties"]["mag"]["ml"])]


def filter_by_magnitude_and_location(size, location, data):
    return [item for item in data if float(size) <= float(item["features"]["properties"]["mag"]["ml"]) and location.upper() in json.dumps(item).upper()]


# === Data Refresh Job ===
def update_data():
    """Refresh AFAD and Kandilli data every few minutes."""
    global afad_data, kandilli_data
    afad_data = fetch_afad()
    kandilli_data = fetch_kandilli()


# Initialize immediately
update_data()
schedule.every(5).minutes.do(update_data)

# === Threaded Scheduler ===
def scheduler_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=scheduler_thread, daemon=True).start()

# === Flask App ===
app = Flask(__name__)


@app.route("/")
def index():
    """API root endpoint with query parameters."""
    source_type = request.args.get("type", "kandilli").lower()
    location = request.args.get("location")
    size = request.args.get("size")

    data = kandilli_data if source_type == "kandilli" else afad_data

    if location and size:
        data = filter_by_magnitude_and_location(size, location, data)
    elif location:
        data = filter_by_location(location, data)
    elif size and size.isnumeric():
        data = filter_by_magnitude(size, data)

    count = len(data)
    response_payload = {
        "type": "FeatureCollection",
        "metadata": {
            "generated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "title": "Mdaedalus Earthquake API",
            "status": count,
            "api_version": "1.0.0",
            "count": count
        },
        "features": data
    }

    response = make_response(json.dumps(response_payload, ensure_ascii=False, indent=2))
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


if __name__ == "__main__":
    print("[INFO] Starting Mdaedalus Earthquake API server...")
    app.run(debug=True)
