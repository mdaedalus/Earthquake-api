# 🌋 Earthquake API

<div align="center">

### Real-time earthquake data from Turkey's two major sources — clean, fast, open.

**Kandilli Rasathanesi (Boğaziçi Üniversitesi) · AFAD (Afet ve Acil Durum Yönetimi Başkanlığı)**

Canlı veri · 5 dakikada bir otomatik güncelleme · GeoJSON uyumlu çıktı · CORS açık

[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](http://makeapullrequest.com)
[![Stars](https://img.shields.io/github/stars/mdaedalus/Earthquake-api?style=for-the-badge&logo=github&color=yellow)](https://github.com/mdaedalus/Earthquake-api)

[🇹🇷 Türkçe](#-türkçe) · [🇬🇧 English](#-english)

</div>

---

<div align="center">

## 🇹🇷 Türkçe

</div>

### 🎯 Nedir Bu?

**Earthquake API**, Türkiye'nin iki büyük deprem veri kaynağından — **Kandilli Rasathanesi** ve **AFAD** — canlı veri çeken, **5 dakikada bir otomatik güncellenen** ve **GeoJSON uyumlu** temiz bir JSON çıktısı sunan hafif bir Flask API'sidir.

Kurulumu saniyeler sürer, harici veritabanı gerektirmez, tüm veriyi bellekte tutar ve web uygulamalarınıza, mobil uygulamalarınıza, harita dashboard'larınıza veya GIS araçlarınıza (Leaflet, Mapbox, QGIS) doğrudan bağlanabilir.

> **Neden Earthquake API?** Çünkü iki ayrı kaynağı tek bir tutarlı şemada birleştirir, bir kaynak düşse bile diğeri çalışmaya devam eder ve thread-safe bir mimariyle Flask'ı asla bloke etmez.

---

### 💡 Neden Bu API?

<div align="center">

| 🌍 | ⏱️ | 🔎 | 📦 |
|:---:|:---:|:---:|:---:|
| **İki kaynak, tek API** | **Otomatik güncelleme** | **Zengin filtreleme** | **GeoJSON uyumlu** |
| Kandilli + AFAD aynı şemada | Her 5 dakikada bir | Konum, büyüklük veya ikisi | Leaflet, Mapbox, QGIS |

| 🧵 | 🛡️ | ❤️ | 🪶 |
|:---:|:---:|:---:|:---:|
| **Thread-safe mimari** | **Hata izolasyonu** | **`/health` endpoint** | **Hafif** |
| `threading.Lock` ile korunur | Bir kaynak düşse diğeri çalışır | Canlılık + tazelik kontrolü | Flask + BS4 + schedule |

</div>

---

### ✨ Özellikler

<table>
<tr>
<td width="50%" valign="top">

#### 🌍 Veri Kaynakları
- ✅ **Kandilli Rasathanesi** canlı akışı
- ✅ **AFAD** resmi akışı
- ✅ Her iki kaynak için **tek ve tutarlı** JSON şeması
- ✅ Türkçe karakter destekli **UTF-8** çıktı

#### ⏱️ Otomatik Güncelleme
- ✅ Arka planda **thread'li scheduler**
- ✅ **5 dakikada bir** otomatik yenileme
- ✅ Başlangıçta **anlık ilk yükleme**
- ✅ Flask'ı bloke etmeyen `daemon=True` thread

#### 🔎 Filtreleme
- ✅ **Konuma göre** — `?location=Izmir`
- ✅ **Büyüklüğe göre** — `?size=4.5`
- ✅ **İkisi birden** — `?size=4&location=Ankara`
- ✅ **Kaynak seçimi** — `?type=afad`

</td>
<td width="50%" valign="top">

#### 📦 Çıktı Formatı
- ✅ **GeoJSON uyumlu** `FeatureCollection`
- ✅ Her deprem: **md / ml / mw** büyüklükleri
- ✅ `geometry`: `{ type: "Point", coordinates: [lon, lat, depth] }`
- ✅ Metadata: `generated`, `last_updated`, `count`, `errors`

#### 🛡️ Güvenilirlik
- ✅ **Per-source** hata izolasyonu
- ✅ **Thread-safe** buffer (`threading.Lock`)
- ✅ **Timeout + User-Agent** ile güvenli istekler
- ✅ JSON dönen **404 ve 500 handler'ları**

#### 🎨 Geliştirici Deneyimi
- ✅ **`/health`** endpoint'i
- ✅ **Açık CORS** politikası
- ✅ `Cache-Control: max-age=60`
- ✅ **MIT** lisansı, ticari kullanıma uygun

</td>
</tr>
</table>

---

### 🛠️ Teknoloji Yığını

<div align="center">

| Katman | Teknoloji |
|:-------|:----------|
| **Backend** | Python 3.10+, Flask 3.0 |
| **HTML Parsing** | BeautifulSoup4 |
| **Zamanlayıcı** | `schedule` + `threading` |
| **HTTP Client** | `urllib` (standart kütüphane) |
| **Eşzamanlılık** | `threading.Lock` (thread-safe buffer) |
| **Çıktı** | JSON (GeoJSON uyumlu) |

</div>

---

### 🚀 Kurulum

#### Gereksinimler
- Python 3.10 veya üzeri
- pip

#### Adım Adım

```bash
# 1. Repoyu klonla
git clone https://github.com/mdaedalus/Earthquake-api.git
cd Earthquake-api

# 2. Sanal ortam oluştur
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. API'yi başlat
python app.py
```

Tarayıcınızda açın: **http://localhost:5000**

> **Not:** `requests` kütüphanesi kullanılmıyor — HTTP istekleri standart kütüphanedeki `urllib` ile yapılıyor.

---

### 🔌 API Kullanımı

#### Kök Endpoint

```http
GET /
```

| Parametre | Tip | Açıklama | Örnek |
|:----------|:----|:---------|:------|
| `type` | string | Kaynak: `kandilli` (varsayılan) veya `afad` | `?type=afad` |
| `location` | string | Şehir / ilçe filtresi (case-insensitive) | `?location=Izmir` |
| `size` | float | Minimum büyüklük (md/ml/mw arasından en büyüğü) | `?size=4.5` |

#### Örnek İstekler

```bash
# Kandilli'den son depremler
curl http://localhost:5000/

# AFAD'dan son depremler
curl http://localhost:5000/?type=afad

# İzmir'deki depremler
curl http://localhost:5000/?location=Izmir

# 4.0 ve üzeri büyüklükteki depremler
curl http://localhost:5000/?size=4

# Ankara'da 3.0 ve üzeri depremler
curl http://localhost:5000/?size=3&location=Ankara

# Sağlık kontrolü
curl http://localhost:5000/health
```

#### Örnek Yanıt

```json
{
  "type": "FeatureCollection",
  "metadata": {
    "generated": "2025-01-15 14:32:00 UTC",
    "last_updated": "2025-01-15 14:30:00 UTC",
    "title": "Earthquake API",
    "api_version": "1.0.0",
    "source": "kandilli",
    "count": 42,
    "errors": {}
  },
  "features": [
    {
      "type": "Feature",
      "properties": {
        "mag": { "md": 0, "ml": 4.2, "mw": 0 },
        "place": "IZMIR KORFEZI",
        "time": 1736958720,
        "updated": 1736958720,
        "status": "İlksel",
        "type": "earthquake",
        "title": "M 4.2 - IZMIR KORFEZI",
        "depth": 7.3
      },
      "geometry": {
        "type": "Point",
        "coordinates": [26.85, 38.42, 7.3]
      },
      "id": "kandilli-1736958720-483921",
      "source": "kandilli"
    }
  ]
}
```

#### Health Endpoint

```http
GET /health
```

```json
{
  "status": "ok",
  "last_updated": "2025-01-15 14:30:00 UTC",
  "kandilli_count": 42,
  "afad_count": 38,
  "errors": {}
}
```

---

### 🗺️ Kullanım Akışı

<div align="center">

| Adres | Yaptığı İş |
|:------|:-----------|
| `/` | Tüm depremler (varsayılan: Kandilli) |
| `/?type=afad` | AFAD kaynağından depremler |
| `/?type=kandilli` | Kandilli kaynağından depremler |
| `/?location=<il>` | Belirtilen ildeki depremler |
| `/?size=<büyüklük>` | Belirtilen büyüklük ve üzeri |
| `/?size=<b>&location=<il>` | Hem konum hem büyüklük filtresi |
| `/health` | Canlılık ve veri tazeliği kontrolü |

</div>

---

### 📂 Proje Yapısı

```
Earthquake-api/
├── app.py                         # Ana Flask uygulaması
├── requirements.txt
├── LICENSE                        # MIT
├── README.md
├── .gitignore
└── img/                           # 📸 Ekran görüntüleri
```

---

### 🔧 Özelleştirme

<details>
<summary><b>⏱️ Güncelleme Sıklığı</b></summary>

`update_data()` çağrısının sıklığını değiştirmek için:

```python
UPDATE_INTERVAL_MINUTES = 5    # 5 dakika
UPDATE_INTERVAL_MINUTES = 1    # 1 dakika
```
</details>

<details>
<summary><b>🌐 Port ve Host</b></summary>

`app.run()` satırını düzenleyin:

```python
app.run(host="0.0.0.0", port=8080, debug=False)
```
</details>

<details>
<summary><b>🔒 CORS Politikası</b></summary>

Tüm domain'lere açmak yerine belirli bir domain'e kısıtlamak için:

```python
response.headers["Access-Control-Allow-Origin"] = "https://siteniz.com"
```
</details>

<details>
<summary><b>🔎 Filtre Genişletme</b></summary>

Yeni filtreler eklemek için `index()` fonksiyonundaki `if/elif` zincirini genişletin:

```python
depth = request.args.get("depth")
if depth:
    data = [d for d in data if d["properties"]["depth"] >= float(depth)]
```
</details>

---

### 🗺️ Yol Haritası

- [x] 🟢 v0.1 — Kandilli scraper
- [x] 🟢 v0.2 — AFAD scraper
- [x] 🟢 v0.3 — Thread'li otomatik güncelleme
- [x] 🟢 v0.4 — Konum & büyüklük filtreleri
- [x] 🟢 v0.5 — GeoJSON uyumlu çıktı
- [x] 🟢 v0.6 — CORS desteği
- [x] 🟢 v0.7 — Thread-safe buffer + `/health` endpoint
- [ ] 🟡 v0.8 — Tarih aralığı filtresi (`?from=2025-01-01&to=2025-01-31`)
- [ ] 🟡 v0.9 — Derinlik filtresi (`?depth=10`)
- [ ] 🟡 v1.0 — CSV / GeoJSON export endpoint'leri
- [ ] 🟠 v1.1 — WebSocket canlı akış
- [ ] 🟠 v1.2 — Redis cache katmanı
- [ ] 🟠 v1.3 — Prometheus metrics
- [ ] 🟠 v1.4 — Rate limiting
- [ ] 🔴 v1.5 — Docker imajı
- [ ] 🔴 v2.0 — Harici deprem API'leri (USGS, EMSC) entegrasyonu

---

### 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Büyük değişiklikler için önce bir **issue** açın.

```bash
# Fork → Clone → Branch → Commit → Push → PR
git checkout -b feature/yeni-ozellik
git commit -m "feat: yeni özellik eklendi"
git push origin feature/yeni-ozellik
```

#### Commit Kuralları

| Prefix | Anlamı |
|:-------|:-------|
| `feat:` | yeni özellik |
| `fix:` | hata düzeltme |
| `docs:` | dokümantasyon |
| `style:` | kod formatı |
| `refactor:` | yeniden düzenleme |
| `test:` | test ekleme |

---

### ⚠️ Yasal Uyarı

Bu API, kamuya açık kaynaklardan (**Kandilli Rasathanesi** ve **AFAD**) veri çeker. Resmî bir kurum değildir ve **acil durum kararları için tek başına kullanılmamalıdır**. Kritik bilgiler için lütfen resmî kaynaklara başvurun:

- 🔗 [Kandilli Rasathanesi](http://www.koeri.boun.edu.tr/scripts/sondepremler.asp)
- 🔗 [AFAD Deprem Dairesi](https://deprem.afad.gov.tr/last-earthquakes.html)

---

<div align="center">

## 🇬🇧 English

</div>

### 🎯 What Is This?

**Earthquake API** is a lightweight Flask API that scrapes live earthquake data from two major Turkish sources — **Kandilli Observatory** and **AFAD** — refreshes automatically every 5 minutes, and exposes a clean **GeoJSON-compatible** JSON output.

It sets up in seconds, requires no external database, holds all data in memory, and plugs directly into your web apps, mobile apps, map dashboards, or GIS tools (Leaflet, Mapbox, QGIS).

> **Why Earthquake API?** Because it merges two sources into one consistent schema, keeps working even if one source goes down, and never blocks Flask thanks to a thread-safe architecture.

---

### 💡 Why This API?

<div align="center">

| 🌍 | ⏱️ | 🔎 | 📦 |
|:---:|:---:|:---:|:---:|
| **Two sources, one API** | **Auto-refresh** | **Rich filtering** | **GeoJSON compatible** |
| Kandilli + AFAD in one schema | Every 5 minutes | Location, magnitude, or both | Leaflet, Mapbox, QGIS |

| 🧵 | 🛡️ | ❤️ | 🪶 |
|:---:|:---:|:---:|:---:|
| **Thread-safe** | **Fault isolation** | **`/health` endpoint** | **Lightweight** |
| Protected by `threading.Lock` | One source down, other keeps running | Liveness + freshness check | Flask + BS4 + schedule |

</div>

---

### ✨ Features

<table>
<tr>
<td width="50%" valign="top">

#### 🌍 Data Sources
- ✅ **Kandilli Observatory** live feed
- ✅ **AFAD** official feed
- ✅ **Single, consistent** JSON schema for both
- ✅ **UTF-8** output with full Turkish support

#### ⏱️ Auto-Refresh
- ✅ Background **threaded scheduler**
- ✅ **Every 5 minutes** automatic refresh
- ✅ **Instant first load** on startup
- ✅ `daemon=True` thread that doesn't block Flask

#### 🔎 Filtering
- ✅ **By location** — `?location=Izmir`
- ✅ **By magnitude** — `?size=4.5`
- ✅ **Both** — `?size=4&location=Ankara`
- ✅ **Source selection** — `?type=afad`

</td>
<td width="50%" valign="top">

#### 📦 Output Format
- ✅ **GeoJSON-compatible** `FeatureCollection`
- ✅ Per quake: **md / ml / mw** magnitudes
- ✅ `geometry`: `{ type: "Point", coordinates: [lon, lat, depth] }`
- ✅ Metadata: `generated`, `last_updated`, `count`, `errors`

#### 🛡️ Reliability
- ✅ **Per-source** error isolation
- ✅ **Thread-safe** buffer (`threading.Lock`)
- ✅ **Timeout + User-Agent** for safe requests
- ✅ JSON **404 & 500 handlers**

#### 🎨 Developer Experience
- ✅ **`/health`** endpoint
- ✅ **Open CORS** policy
- ✅ `Cache-Control: max-age=60`
- ✅ **MIT** license, commercial use OK

</td>
</tr>
</table>

---

### 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|:------|:-----------|
| **Backend** | Python 3.10+, Flask 3.0 |
| **HTML Parsing** | BeautifulSoup4 |
| **Scheduler** | `schedule` + `threading` |
| **HTTP Client** | `urllib` (standard library) |
| **Concurrency** | `threading.Lock` (thread-safe buffer) |
| **Output** | JSON (GeoJSON-compatible) |

</div>

---

### 🚀 Installation

#### Requirements
- Python 3.10 or higher
- pip

#### Step by Step

```bash
# 1. Clone the repo
git clone https://github.com/mdaedalus/Earthquake-api.git
cd Earthquake-api

# 2. Create virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the API
python app.py
```

Open in your browser: **http://localhost:5000**

> **Note:** `requests` is not used — HTTP calls go through the standard library's `urllib`.

---

### 🔌 API Usage

#### Root Endpoint

```http
GET /
```

| Parameter | Type | Description | Example |
|:----------|:-----|:------------|:--------|
| `type` | string | Source: `kandilli` (default) or `afad` | `?type=afad` |
| `location` | string | City / district filter (case-insensitive) | `?location=Izmir` |
| `size` | float | Minimum magnitude (largest of md/ml/mw) | `?size=4.5` |

#### Example Requests

```bash
# Latest earthquakes from Kandilli
curl http://localhost:5000/

# Latest earthquakes from AFAD
curl http://localhost:5000/?type=afad

# Earthquakes in Izmir
curl http://localhost:5000/?location=Izmir

# Earthquakes of magnitude 4.0 and above
curl http://localhost:5000/?size=4

# Earthquakes of magnitude 3.0+ in Ankara
curl http://localhost:5000/?size=3&location=Ankara

# Health check
curl http://localhost:5000/health
```

#### Example Response

```json
{
  "type": "FeatureCollection",
  "metadata": {
    "generated": "2025-01-15 14:32:00 UTC",
    "last_updated": "2025-01-15 14:30:00 UTC",
    "title": "Earthquake API",
    "api_version": "1.0.0",
    "source": "kandilli",
    "count": 42,
    "errors": {}
  },
  "features": [
    {
      "type": "Feature",
      "properties": {
        "mag": { "md": 0, "ml": 4.2, "mw": 0 },
        "place": "IZMIR KORFEZI",
        "time": 1736958720,
        "updated": 1736958720,
        "status": "İlksel",
        "type": "earthquake",
        "title": "M 4.2 - IZMIR KORFEZI",
        "depth": 7.3
      },
      "geometry": {
        "type": "Point",
        "coordinates": [26.85, 38.42, 7.3]
      },
      "id": "kandilli-1736958720-483921",
      "source": "kandilli"
    }
  ]
}
```

#### Health Endpoint

```http
GET /health
```

```json
{
  "status": "ok",
  "last_updated": "2025-01-15 14:30:00 UTC",
  "kandilli_count": 42,
  "afad_count": 38,
  "errors": {}
}
```

---

### 🗺️ Usage Flow

<div align="center">

| URL | What It Does |
|:----|:-------------|
| `/` | All earthquakes (default: Kandilli) |
| `/?type=afad` | Earthquakes from AFAD |
| `/?type=kandilli` | Earthquakes from Kandilli |
| `/?location=<city>` | Earthquakes in the given city |
| `/?size=<magnitude>` | Earthquakes at or above magnitude |
| `/?size=<m>&location=<city>` | Both filters combined |
| `/health` | Liveness & data freshness check |

</div>

---

### 📂 Project Structure

```
Earthquake-api/
├── app.py                         # Main Flask app
├── requirements.txt
├── LICENSE                        # MIT
├── README.md
├── .gitignore
└── img/                           # 📸 Screenshots
```

---

### 🔧 Customization

<details>
<summary><b>⏱️ Refresh Interval</b></summary>

To change how often `update_data()` runs:

```python
UPDATE_INTERVAL_MINUTES = 5    # 5 minutes
UPDATE_INTERVAL_MINUTES = 1    # 1 minute
```
</details>

<details>
<summary><b>🌐 Port and Host</b></summary>

Edit the `app.run()` line:

```python
app.run(host="0.0.0.0", port=8080, debug=False)
```
</details>

<details>
<summary><b>🔒 CORS Policy</b></summary>

To restrict CORS to a specific domain instead of opening it to all:

```python
response.headers["Access-Control-Allow-Origin"] = "https://yourdomain.com"
```
</details>

<details>
<summary><b>🔎 Extending Filters</b></summary>

Add new filters by extending the `if/elif` chain in `index()`:

```python
depth = request.args.get("depth")
if depth:
    data = [d for d in data if d["properties"]["depth"] >= float(depth)]
```
</details>

---

### 🗺️ Roadmap

- [x] 🟢 v0.1 — Kandilli scraper
- [x] 🟢 v0.2 — AFAD scraper
- [x] 🟢 v0.3 — Threaded auto-refresh
- [x] 🟢 v0.4 — Location & magnitude filters
- [x] 🟢 v0.5 — GeoJSON-compatible output
- [x] 🟢 v0.6 — CORS support
- [x] 🟢 v0.7 — Thread-safe buffer + `/health` endpoint
- [ ] 🟡 v0.8 — Date range filter (`?from=2025-01-01&to=2025-01-31`)
- [ ] 🟡 v0.9 — Depth filter (`?depth=10`)
- [ ] 🟡 v1.0 — CSV / GeoJSON export endpoints
- [ ] 🟠 v1.1 — WebSocket live stream
- [ ] 🟠 v1.2 — Redis cache layer
- [ ] 🟠 v1.3 — Prometheus metrics
- [ ] 🟠 v1.4 — Rate limiting
- [ ] 🔴 v1.5 — Docker image
- [ ] 🔴 v2.0 — External earthquake APIs (USGS, EMSC) integration

---

### 🤝 Contributing

Contributions are welcome! For major changes, please open an **issue** first.

```bash
# Fork → Clone → Branch → Commit → Push → PR
git checkout -b feature/new-feature
git commit -m "feat: added new feature"
git push origin feature/new-feature
```

#### Commit Conventions

| Prefix | Meaning |
|:-------|:--------|
| `feat:` | new feature |
| `fix:` | bug fix |
| `docs:` | documentation |
| `style:` | code formatting |
| `refactor:` | refactoring |
| `test:` | adding tests |

---

### ⚠️ Disclaimer

This API scrapes data from publicly available sources (**Kandilli Observatory** and **AFAD**). It is **not** an official body and **must not be used as the sole basis for emergency decisions**. Always refer to official sources for critical information:

- 🔗 [Kandilli Observatory](http://www.koeri.boun.edu.tr/scripts/sondepremler.asp)
- 🔗 [AFAD Earthquake Department](https://deprem.afad.gov.tr/last-earthquakes.html)

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

<div align="center">

**Emin Neşat Gürses**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Emin_Neşat_Gürses-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/emin-ne%C5%9Fat-g%C3%BCrses-35723a284/)
[![Email](https://img.shields.io/badge/Email-eminnesatg@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:eminnesatg@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-@mdaedalus-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mdaedalus)

</div>

---

<div align="center">

### ⭐ If you like this project, don't forget to star it!

[![Star](https://img.shields.io/badge/⭐_Star_this_repo-yellow?style=for-the-badge)](https://github.com/mdaedalus/Earthquake-api)
[![Report Bug](https://img.shields.io/badge/🐛_Report_Bug-red?style=for-the-badge)](https://github.com/mdaedalus/Earthquake-api/issues)
[![Request Feature](https://img.shields.io/badge/💡_Request_Feature-blue?style=for-the-badge)](https://github.com/mdaedalus/Earthquake-api/issues)

**Made with ❤️ in Turkey**

</div>
