from typing import Any, Dict, List
import requests

def nominatim_amenity_search(
    lat: float,
    lon: float,
    radius_m: int,
    place_type: str,
    limit: int,
    nominatim_url: str,
    user_agent: str,
    email: str,
    timeout_s: int,
) -> List[Dict[str, Any]]:
    headers = {"User-Agent": user_agent, "Accept": "application/json"}
    params = {
        "format": "json",
        "limit": max(1, int(limit)),
        "amenity": place_type,
        "viewbox": _viewbox(lat, lon, radius_m),
        "bounded": 1,
        "email": email,
    }
    r = requests.get(nominatim_url, params=params, headers=headers, timeout=timeout_s)
    r.raise_for_status()
    data = r.json()
    items: List[Dict[str, Any]] = []
    for it in data:
        try:
            items.append({
                "id": int(it.get("osm_id")) if it.get("osm_id") else None,
                "osm_type": it.get("osm_type"),
                "name": it.get("display_name", "Unknown").split(",")[0],
                "lat": float(it["lat"]),
                "lon": float(it["lon"]),
                "address": it.get("display_name"),
                "phone": None,
                "website": None,
                "opening_hours": None,
                "tags": {},
            })
        except Exception:
            continue
    return items

def _viewbox(lat: float, lon: float, radius_m: int) -> str:
    d = max(50, int(radius_m))
    deg = d / 111_000
    left = lon - deg
    right = lon + deg
    top = lat + deg
    bottom = lat - deg
    return f"{left},{top},{right},{bottom}"
