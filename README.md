# 🌋 Mdaedalus Earthquake API

**Mdaedalus Earthquake API** is a real-time Flask-based API that aggregates earthquake data from two major Turkish data sources:  
- **Kandilli Observatory (Boğaziçi University)**  
- **AFAD (Disaster and Emergency Management Authority)**  

The service automatically updates every 5 minutes and exposes a clean JSON interface compatible with GIS tools, dashboards, and frontend clients.

---

## 🚀 Key Features

- Scrapes **live earthquake data** from Kandilli and AFAD
- Auto-refreshes every **5 minutes** using background threads
- Supports **filtering** by:
  - Location (`?location=Izmir`)
  - Magnitude (`?size=4`)
  - Both (`?size=4&location=Ankara`)
- Returns consistent **GeoJSON-like structure**
- Open **CORS** policy for web integration

---

## 📂 Project Structure

mdaedalus_earthquake_api/
├── mdaedalus_earthquake_api.py
└── README.md


---

## ⚙️ Requirements

Install the dependencies:

```bash
pip install flask beautifulsoup4 schedule requests
