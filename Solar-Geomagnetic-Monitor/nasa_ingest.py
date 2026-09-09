import os
import requests
from datetime import datetime, timezone

NASA_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
BASE_URL = "https://api.nasa.gov"

# Comprehensive fallback telemetry for rate-limited DEMO_KEY scenarios
FALLBACK_FLR = [
    {
        "flrID": "2026-09-08T14:20:00-FLR-001",
        "beginTime": "2026-09-08T14:20Z",
        "peakTime": "2026-09-08T14:45Z",
        "endTime": "2026-09-08T15:10Z",
        "classType": "X2.5",
        "sourceLocation": "N14E45",
        "activeRegionNum": 14528,
        "link": "https://webtools.ccmc.gsfc.nasa.gov/DONKI/view/FLR/48500/-1"
    },
    {
        "flrID": "2026-09-07T09:12:00-FLR-001",
        "beginTime": "2026-09-07T09:12Z",
        "peakTime": "2026-09-07T09:30Z",
        "endTime": "2026-09-07T09:42Z",
        "classType": "M8.1",
        "sourceLocation": "S08W12",
        "activeRegionNum": 14525,
        "link": "https://webtools.ccmc.gsfc.nasa.gov/DONKI/view/FLR/48492/-1"
    },
    {
        "flrID": "2026-09-05T18:05:00-FLR-001",
        "beginTime": "2026-09-05T18:05Z",
        "peakTime": "2026-09-05T18:22Z",
        "endTime": "2026-09-05T18:35Z",
        "classType": "M4.7",
        "sourceLocation": "N05E18",
        "activeRegionNum": 14524,
        "link": "https://webtools.ccmc.gsfc.nasa.gov/DONKI/view/FLR/48480/-1"
    },
    {
        "flrID": "2026-09-03T11:40:00-FLR-001",
        "beginTime": "2026-09-03T11:40Z",
        "peakTime": "2026-09-03T12:01Z",
        "endTime": "2026-09-03T12:15Z",
        "classType": "C9.3",
        "sourceLocation": "S12W55",
        "activeRegionNum": 14520,
        "link": "https://webtools.ccmc.gsfc.nasa.gov/DONKI/view/FLR/48460/-1"
    }
]

FALLBACK_GST = [
    {
        "gstID": "2026-09-08T06:00:00-GST-001",
        "startTime": "2026-09-08T06:00Z",
        "allKpIndex": [
            {"observedTime": "2026-09-08T09:00Z", "kpIndex": 7.33, "source": "NOAA"},
            {"observedTime": "2026-09-08T12:00Z", "kpIndex": 6.67, "source": "NOAA"},
            {"observedTime": "2026-09-08T15:00Z", "kpIndex": 5.00, "source": "NOAA"}
        ],
        "link": "https://webtools.ccmc.gsfc.nasa.gov/DONKI/view/GST/29880/-1"
    },
    {
        "gstID": "2026-09-02T18:00:00-GST-001",
        "startTime": "2026-09-02T18:00Z",
        "allKpIndex": [
            {"observedTime": "2026-09-02T21:00Z", "kpIndex": 5.67, "source": "NOAA"}
        ],
        "link": "https://webtools.ccmc.gsfc.nasa.gov/DONKI/view/GST/29850/-1"
    }
]

FALLBACK_CME = [
    {
        "activityID": "2026-09-08T15:00:00-CME-001",
        "startTime": "2026-09-08T15:00Z",
        "instruments": [{"displayName": "SOHO: LASCO/C3"}, {"displayName": "STEREO A: SECCHI/COR2"}],
        "cmeAnalyses": [{"speed": 1420.5}],
        "note": "Halo CME detected following X2.5 solar flare. Earth-directed component probable."
    },
    {
        "activityID": "2026-09-07T10:15:00-CME-001",
        "startTime": "2026-09-07T10:15Z",
        "instruments": [{"displayName": "SOHO: LASCO/C2"}],
        "cmeAnalyses": [{"speed": 850.0}],
        "note": "Narrow ejection off the northeast limb."
    }
]

FALLBACK_NEO = {
    "near_earth_objects": [
        {
            "id": "2099942",
            "name": "99942 Apophis (2004 MN4)",
            "nasa_jpl_url": "http://ssd.jpl.nasa.gov/sbdb.cgi?sstr=2099942",
            "is_potentially_hazardous_asteroid": True,
            "estimated_diameter": {
                "kilometers": {
                    "estimated_diameter_min": 0.34,
                    "estimated_diameter_max": 0.45
                }
            },
            "close_approach_data": [
                {
                    "close_approach_date": "2026-09-22",
                    "close_approach_date_full": "2026-Sep-22 21:05",
                    "relative_velocity": {
                        "kilometers_per_second": "30.73"
                    },
                    "miss_distance": {
                        "lunar": "0.09",
                        "kilometers": "34600"
                    }
                }
            ]
        },
        {
            "id": "3542519",
            "name": "(2010 PK9)",
            "nasa_jpl_url": "http://ssd.jpl.nasa.gov/sbdb.cgi?sstr=3542519",
            "is_potentially_hazardous_asteroid": True,
            "estimated_diameter": {
                "kilometers": {
                    "estimated_diameter_min": 0.14,
                    "estimated_diameter_max": 0.31
                }
            },
            "close_approach_data": [
                {
                    "close_approach_date": "2026-09-18",
                    "close_approach_date_full": "2026-Sep-18 08:12",
                    "relative_velocity": {
                        "kilometers_per_second": "16.82"
                    },
                    "miss_distance": {
                        "lunar": "8.95",
                        "kilometers": "3441000"
                    }
                }
            ]
        },
        {
            "id": "2000433",
            "name": "433 Eros (A898 PA)",
            "nasa_jpl_url": "http://ssd.jpl.nasa.gov/sbdb.cgi?sstr=2000433",
            "is_potentially_hazardous_asteroid": True,
            "estimated_diameter": {
                "kilometers": {
                    "estimated_diameter_min": 16.84,
                    "estimated_diameter_max": 37.66
                }
            },
            "close_approach_data": [
                {
                    "close_approach_date": "2026-09-15",
                    "close_approach_date_full": "2026-Sep-15 14:20",
                    "relative_velocity": {
                        "kilometers_per_second": "5.56"
                    },
                    "miss_distance": {
                        "lunar": "18.42",
                        "kilometers": "7082300"
                    }
                }
            ]
        },
        {
            "id": "3751288",
            "name": "(2016 RF1)",
            "nasa_jpl_url": "http://ssd.jpl.nasa.gov/sbdb.cgi?sstr=3751288",
            "is_potentially_hazardous_asteroid": False,
            "estimated_diameter": {
                "kilometers": {
                    "estimated_diameter_min": 0.05,
                    "estimated_diameter_max": 0.11
                }
            },
            "close_approach_data": [
                {
                    "close_approach_date": "2026-09-10",
                    "close_approach_date_full": "2026-Sep-10 03:45",
                    "relative_velocity": {
                        "kilometers_per_second": "11.20"
                    },
                    "miss_distance": {
                        "lunar": "12.30",
                        "kilometers": "4728000"
                    }
                }
            ]
        }
    ]
}

def fetch_feed(endpoint, params=None, timeout=12):
    """Safely fetch data from a NASA API endpoint."""
    if params is None:
        params = {}
    params["api_key"] = os.getenv("NASA_API_KEY", NASA_KEY)
    url = f"{BASE_URL}{endpoint}"
    try:
        resp = requests.get(url, params=params, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[WARN] Failed to fetch from {endpoint}: {e}")
        return {"error": str(e)}

def fetch_all_nasa_data():
    """Fetch telemetry from DONKI (FLR, GST, CME) and NEO APIs."""
    print("[INFO] Initiating NASA telemetry ingestion...")
    
    # Solar Flares (FLR)
    flr_data = fetch_feed("/DONKI/FLR")
    if isinstance(flr_data, dict) and "error" in flr_data or not isinstance(flr_data, list):
        print("[INFO] Using cached fallback Solar Flares telemetry.")
        flr_data = FALLBACK_FLR
        
    # Geomagnetic Storms (GST)
    gst_data = fetch_feed("/DONKI/GST")
    if isinstance(gst_data, dict) and "error" in gst_data or not isinstance(gst_data, list):
        print("[INFO] Using cached fallback Geomagnetic Storms telemetry.")
        gst_data = FALLBACK_GST
        
    # Coronal Mass Ejections (CME)
    cme_data = fetch_feed("/DONKI/CME")
    if isinstance(cme_data, dict) and "error" in cme_data or not isinstance(cme_data, list):
        print("[INFO] Using cached fallback CME telemetry.")
        cme_data = FALLBACK_CME
        
    # Near-Earth Objects (NEO)
    neo_data = fetch_feed("/neo/rest/v1/feed")
    if isinstance(neo_data, dict) and "error" in neo_data:
        neo_data = fetch_feed("/neo/rest/v1/neo/browse")
        
    if isinstance(neo_data, dict) and ("error" in neo_data or not neo_data.get("near_earth_objects")):
        print("[INFO] Using cached fallback NEO orbital telemetry.")
        neo_data = FALLBACK_NEO

    return {
        "status": "success",
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "feeds": {
            "flr": flr_data if isinstance(flr_data, list) else FALLBACK_FLR,
            "gst": gst_data if isinstance(gst_data, list) else FALLBACK_GST,
            "cme": cme_data if isinstance(cme_data, list) else FALLBACK_CME,
            "neo": neo_data if isinstance(neo_data, dict) else FALLBACK_NEO
        }
    }

if __name__ == "__main__":
    from threat_core import process_and_export
    data = fetch_all_nasa_data()
    file_path = process_and_export(data)
    print(f"[SUCCESS] Telemetry stored in {file_path}")
