import json
import os
from flask import Flask, jsonify, send_from_directory, request

app = Flask(__name__, static_folder=None)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "threats.json")

def load_or_refresh_data():
    """Ensure threats.json exists and load it."""
    if not os.path.exists(DATA_FILE):
        try:
            from nasa_ingest import fetch_all_nasa_data
            from threat_core import process_and_export
            data = fetch_all_nasa_data()
            process_and_export(data, filename=DATA_FILE)
        except Exception as e:
            return {"status": "error", "message": str(e), "feeds": {}}
            
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"status": "error", "message": f"Failed to read threats.json: {e}"}

@app.get("/")
def home():
    """Serve the Mission Control Dashboard HTML page."""
    return send_from_directory(BASE_DIR, "dashboard.html")

@app.get("/api/space-weather")
@app.get("/api/threats")
def get_threats():
    """Return full space weather telemetry and threat analytics."""
    data = load_or_refresh_data()
    return jsonify(data)

@app.get("/api/near-earth-objects")
def get_neos():
    """Return normalized tracked Near-Earth Objects."""
    data = load_or_refresh_data()
    neos = data.get("analytics", {}).get("near_earth_objects", [])
    if not neos:
        # Fallback to raw feeds structure
        raw_neo = data.get("feeds", {}).get("neo", {})
        if isinstance(raw_neo, dict):
            neos = raw_neo.get("near_earth_objects", [])
    return jsonify({"objects": neos})

@app.route("/api/refresh", methods=["GET", "POST"])
def refresh_telemetry():
    """Trigger live fetch from NASA APIs and update local data store."""
    try:
        from nasa_ingest import fetch_all_nasa_data
        from threat_core import process_and_export
        raw_data = fetch_all_nasa_data()
        process_and_export(raw_data, filename=DATA_FILE)
        updated_data = load_or_refresh_data()
        return jsonify({
            "status": "success",
            "message": "Telemetry refreshed successfully.",
            "data": updated_data
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Refresh failed: {str(e)}"
        }), 500

@app.get("/api/health")
def health():
    """System health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "NASA Telemetry Command Console",
        "data_file_exists": os.path.exists(DATA_FILE)
    })

if __name__ == "__main__":
    print("[INFO] Starting NASA Telemetry Command Console server on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
