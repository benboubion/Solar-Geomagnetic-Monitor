# 🚀 NASA Space Telemetry & Orbital Hazard Command Console

A real-time telemetry ingestion engine, threat analytics scoring system, and interactive glassmorphic Mission Control dashboard powered by official NASA APIs (DONKI & NeoWs).

![Dashboard Interface](dashboard.html)

---

## 🌟 Key Features

* **☀️ Solar Flare Monitoring (FLR)**: Real-time class severity calculation ($X$, $M$, $C$-Class flares) with source active region tracking.
* **🛡️ Geomagnetic Storm Radar (GST)**: Tracks peak $K_p$ indices and storm severity readouts from NOAA & NASA DONKI sensors.
* **☄️ Near-Earth Object Radar (NEO)**: Tracks close-approach planetary passings, lunar distance margins, estimated diameters, and velocity vectors.
* **🌌 Coronal Mass Ejection Vectors (CME)**: Monitors solar coronal mass ejection velocities and instrument readouts.
* **⚠️ DEFCON & Space Threat Index**: Dynamic algorithm computing space weather threat level (DEFCON 1 to 5) and aggregate risk index (0–100).
* **⚡ Self-Healing Telemetry & Live Sync**: Auto-ingests telemetry on server boot if missing; supports rate-limited `DEMO_KEY` with cached fallback data.

---

## 🚀 Quick Start Guide

### 1. Clone & Prerequisites

Ensure you have Python 3.8+ installed:

```bash
git clone https://github.com/benboubion/Solar-Geomagnetic-Monitor.git
cd Solar-Geomagnetic-Monitor
pip install -r requirements.txt
```

### 2. Set API Key (Optional)

By default, the system uses NASA's public `DEMO_KEY`. To use your custom NASA API key:

* **Linux / macOS**:
  ```bash
  export NASA_API_KEY="YOUR_NASA_API_KEY"
  ```
* **Windows (Command Prompt / PowerShell)**:
  ```powershell
  $env:NASA_API_KEY="YOUR_NASA_API_KEY"
  ```

*(You can request a free API key at [api.nasa.gov](https://api.nasa.gov))*

### 3. Launch Mission Control

Run the ingest script manually or start the server directly (the server auto-fetches data if `threats.json` does not exist):

```bash
python server.py
```

Navigate to **`http://127.0.0.1:5000`** in your web browser.

---

## 📁 Repository Architecture

```text
.
├── dashboard.html     # Mission Control web interface
├── nasa_ingest.py     # NASA REST API fetcher (DONKI & NeoWs feeds + fallbacks)
├── threat_core.py     # Hazard scoring algorithms & DEFCON index calculation
├── server.py          # Flask HTTP backend & API telemetry provider
├── requirements.txt   # Python dependencies (Flask, requests)
└── .gitignore         # Git rules (excludes runtime threats.json & secrets)
```

---

## 🛠️ API Reference Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Serves the Mission Control dashboard frontend |
| `/api/space-weather` | `GET` | Returns full enriched space weather telemetry & analytics |
| `/api/near-earth-objects` | `GET` | Returns list of tracked Near-Earth Asteroids |
| `/api/refresh` | `POST / GET` | Triggers immediate live API fetch from NASA servers |
| `/api/health` | `GET` | System health check & data file validation |

---

## 🔒 Security & Privacy

* **No Hardcoded Secrets**: All API key logic references environment variables (`NASA_API_KEY`) or public demo keys.
* **Excluded Runtime Data**: `threats.json` and `.env` files are ignored by git to keep your repository clean and secure.

---
