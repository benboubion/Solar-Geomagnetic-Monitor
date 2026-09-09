# Space Telemetry Dashboard — Setup

## Quick Start
1. Set env: `set "NASA_API_KEY=YOUR_KEY"`
2. Fetch live feeds: `python nasa_ingest.py`
3. Start server: `python server.py`
4. Browse `http://127.0.0.1:5000/`

## What's Included
- `nasa_ingest.py` — pulls DONKI FLR/CME/GST + NEO feeds
- `threat_core.py` — scoring/filtering logic
- `server.py` — Flask backend (`/api/space-weather`)

## Notes
- Key is kept out of source; set via environment only.
- `threats.json` is generated at runtime by ingest — do not commit live data.
- For GitHub upload: do not include `threats.json` or your `.env`; only commit source.
