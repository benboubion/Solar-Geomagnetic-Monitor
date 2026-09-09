import json
import os
import re
from datetime import datetime, timezone

def parse_class_score(class_type):
    """Calculate a numeric severity score for solar flares (e.g. X1.5 -> 150, M2.0 -> 20)."""
    if not class_type or not isinstance(class_type, str):
        return 1.0
    match = re.match(r"([XMCBA])([\d\.]*)", class_type.upper())
    if not match:
        return 1.0
    letter, val_str = match.groups()
    multiplier = {"X": 100, "M": 10, "C": 1, "B": 0.1, "A": 0.01}.get(letter, 1)
    try:
        val = float(val_str) if val_str else 1.0
    except ValueError:
        val = 1.0
    return round(multiplier * val, 2)

def score_solar(flares):
    """Analyze and score solar flare events."""
    scored = []
    if not isinstance(flares, list):
        return scored
    
    for f in flares:
        if not isinstance(f, dict):
            continue
        c_type = f.get("classType", "") or ""
        score = parse_class_score(c_type)
        
        if c_type.startswith("X"):
            hazard = "CRITICAL"
        elif c_type.startswith("M"):
            hazard = "HIGH"
        elif c_type.startswith("C"):
            hazard = "MODERATE"
        else:
            hazard = "LOW"
            
        scored.append({
            "id": f.get("flrID", "UNKNOWN"),
            "classType": c_type,
            "hazard": hazard,
            "severity_score": score,
            "beginTime": f.get("beginTime"),
            "peakTime": f.get("peakTime"),
            "sourceLocation": f.get("sourceLocation") or "N/A",
            "activeRegionNum": f.get("activeRegionNum"),
            "link": f.get("link")
        })
    # Sort by severity score descending
    scored.sort(key=lambda x: x["severity_score"], reverse=True)
    return scored

def score_neos(neo_data):
    """Analyze and score Near-Earth Objects from feed or browse endpoints."""
    objects_list = []
    if isinstance(neo_data, dict):
        if "near_earth_objects" in neo_data:
            neo_field = neo_data["near_earth_objects"]
            if isinstance(neo_field, dict):
                # Feed format: dict of date keys -> list of objects
                for date_key, items in neo_field.items():
                    if isinstance(items, list):
                        objects_list.extend(items)
            elif isinstance(neo_field, list):
                # Browse format: list of objects directly
                objects_list.extend(neo_field)
    
    scored = []
    for a in objects_list:
        if not isinstance(a, dict):
            continue
            
        name = a.get("name", "Unknown Asteroid")
        is_haz = bool(a.get("is_potentially_hazardous_asteroid", False))
        
        diam_dict = a.get("estimated_diameter", {}).get("kilometers", {})
        diam_max = diam_dict.get("estimated_diameter_max", 0.0) or 0.0
        diam_min = diam_dict.get("estimated_diameter_min", 0.0) or 0.0
        
        cad_list = a.get("close_approach_data", [])
        cad = cad_list[0] if cad_list and isinstance(cad_list[0], dict) else {}
        
        miss_lunar = 999.0
        miss_km = 999999999.0
        vel_km_s = 0.0
        approach_date = cad.get("close_approach_date_full") or cad.get("close_approach_date") or "N/A"
        
        try:
            miss_lunar = float(cad.get("miss_distance", {}).get("lunar", 999.0))
        except (ValueError, TypeError):
            pass
            
        try:
            miss_km = float(cad.get("miss_distance", {}).get("kilometers", 999999999.0))
        except (ValueError, TypeError):
            pass
            
        try:
            vel_km_s = float(cad.get("relative_velocity", {}).get("kilometers_per_second", 0.0))
        except (ValueError, TypeError):
            pass
            
        # Determine threat classification
        if is_haz and miss_lunar < 15.0:
            threat = "CRITICAL"
        elif is_haz or miss_lunar < 10.0:
            threat = "HIGH"
        elif miss_lunar < 30.0 or diam_max > 0.5:
            threat = "MODERATE"
        else:
            threat = "LOW"
            
        scored.append({
            "name": name,
            "id": a.get("id"),
            "nasa_jpl_url": a.get("nasa_jpl_url"),
            "is_potentially_hazardous": is_haz,
            "estimated_diameter_km_max": round(diam_max, 3),
            "estimated_diameter_km_min": round(diam_min, 3),
            "miss_distance_lunar": round(miss_lunar, 2),
            "miss_distance_km": round(miss_km, 1),
            "vel_km_s": round(vel_km_s, 2),
            "approach_date": approach_date,
            "threat_level": threat
        })
        
    scored.sort(key=lambda x: (x["is_potentially_hazardous"], -x["estimated_diameter_km_max"]), reverse=True)
    return scored

def score_storms(storms):
    """Analyze and score Geomagnetic Storms (GST)."""
    scored = []
    if not isinstance(storms, list):
        return scored
        
    for s in storms:
        if not isinstance(s, dict):
            continue
        kp_indices = s.get("allKpIndex", [])
        kp_vals = []
        if isinstance(kp_indices, list):
            for k in kp_indices:
                if isinstance(k, dict) and "kpIndex" in k:
                    try:
                        kp_vals.append(float(k["kpIndex"]))
                    except (ValueError, TypeError):
                        pass
        max_kp = max(kp_vals) if kp_vals else 0.0
        
        if max_kp >= 8.0:
            threat = "CRITICAL"
        elif max_kp >= 6.0:
            threat = "HIGH"
        elif max_kp >= 5.0:
            threat = "MODERATE"
        else:
            threat = "LOW"
            
        scored.append({
            "id": s.get("gstID", "UNKNOWN"),
            "startTime": s.get("startTime"),
            "max_kp": round(max_kp, 2),
            "kp_count": len(kp_vals),
            "threat_level": threat,
            "link": s.get("link")
        })
    scored.sort(key=lambda x: x["max_kp"], reverse=True)
    return scored

def score_cmes(cmes):
    """Analyze Coronal Mass Ejections (CME)."""
    scored = []
    if not isinstance(cmes, list):
        return scored
    for c in cmes:
        if not isinstance(c, dict):
            continue
        instruments = [i.get("displayName") for i in c.get("instruments", []) if isinstance(i, dict)]
        cme_analyses = c.get("cmeAnalyses", [])
        speed = 0.0
        if cme_analyses and isinstance(cme_analyses[0], dict):
            speed = cme_analyses[0].get("speed", 0.0) or 0.0
        scored.append({
            "id": c.get("activityID", "UNKNOWN"),
            "startTime": c.get("startTime"),
            "instruments": instruments,
            "speed_km_s": round(float(speed), 1) if speed else "N/A",
            "note": c.get("note", "") or "No notes"
        })
    return scored

def calculate_defcon(solar_scored, neo_scored, storm_scored):
    """Calculate space threat index (0-100) and DEFCON level (1 to 5)."""
    score = 0
    # Solar Flares impact
    critical_flares = sum(1 for f in solar_scored if f["hazard"] == "CRITICAL")
    high_flares = sum(1 for f in solar_scored if f["hazard"] == "HIGH")
    score += critical_flares * 25 + high_flares * 10
    
    # NEO impact
    crit_neos = sum(1 for n in neo_scored if n["threat_level"] == "CRITICAL")
    haz_neos = sum(1 for n in neo_scored if n["is_potentially_hazardous"])
    score += crit_neos * 30 + haz_neos * 8
    
    # Storms impact
    severe_storms = sum(1 for s in storm_scored if s["threat_level"] in ("CRITICAL", "HIGH"))
    score += severe_storms * 15
    
    threat_index = min(100, score)
    
    if threat_index >= 75:
        defcon = 1 # MAXIMUM ALERT
    elif threat_index >= 50:
        defcon = 2 # ELEVATED RISK
    elif threat_index >= 30:
        defcon = 3 # MODERATE MONITORING
    elif threat_index >= 15:
        defcon = 4 # ADVISORY
    else:
        defcon = 5 # NORMAL
        
    return defcon, threat_index

def process_and_export(raw_data, filename="threats.json"):
    """Enrich raw telemetry data with hazard analytics and write to JSON file."""
    feeds = raw_data.get("feeds", {})
    
    flr_raw = feeds.get("flr", [])
    neo_raw = feeds.get("neo", {})
    gst_raw = feeds.get("gst", [])
    cme_raw = feeds.get("cme", [])
    
    flr_scored = score_solar(flr_raw if isinstance(flr_raw, list) else [])
    neo_scored = score_neos(neo_raw if isinstance(neo_raw, dict) else {})
    gst_scored = score_storms(gst_raw if isinstance(gst_raw, list) else [])
    cme_scored = score_cmes(cme_raw if isinstance(cme_raw, list) else [])
    
    defcon, threat_index = calculate_defcon(flr_scored, neo_scored, gst_scored)
    
    enriched = {
        "status": "active",
        "last_updated": raw_data.get("last_updated", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")),
        "threat_summary": {
            "defcon_level": defcon,
            "threat_index": threat_index,
            "total_flares": len(flr_scored),
            "critical_flares": sum(1 for f in flr_scored if f["hazard"] == "CRITICAL"),
            "total_neos_tracked": len(neo_scored),
            "hazardous_neos": sum(1 for n in neo_scored if n["is_potentially_hazardous"]),
            "active_storms": len(gst_scored),
            "cme_events": len(cme_scored)
        },
        "analytics": {
            "solar_flares": flr_scored,
            "near_earth_objects": neo_scored,
            "geomagnetic_storms": gst_scored,
            "cme_events": cme_scored
        },
        "feeds": feeds # Preserve raw feeds for backward compatibility
    }
    
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2)
        
    return filepath

def export(hazards):
    """Legacy helper function."""
    return process_and_export({"feeds": hazards})
