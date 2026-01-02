from typing import Any, Dict, List, Tuple
import requests

_PLACE_TAGS: dict[str, Tuple[str, str]] = {
    "pharmacy": ("amenity", "pharmacy"),
    "hospital": ("amenity", "hospital"),
    "clinic": ("amenity", "clinic"),
    "doctors": ("amenity", "doctors"),
    "dentist": ("amenity", "dentist"),
}

def _build_overpass_query(lat: float, lon: float, radius_m: int, place_type: str, limit: int) -> str:
    k, v = _PLACE_TAGS.get(place_type, _PLACE_TAGS["pharmacy"])
    lim = max(1, int(limit))
    rad = max(50, int(radius_m))
    return f"""
[out:json][timeout:45];
node(around:{rad},{lat},{lon})["{k}"="{v}"];
out {lim};
""".strip()

def overpass_search(
    lat: float,
    lon: float,
    radius_m: int,
    place_type: str,
    limit: int,
    overpass_url: str,
    timeout_s: int,
    retries: int,
) -> List[Dict[str, Any]]:
    q = _build_overpass_query(lat, lon, radius_m, place_type, limit)
    last_err: Exception | None = None
    for _ in range(max(1, retries + 1)):
        try:
            r = requests.post(
                overpass_url,
                data=q.encode("utf-8"),
                headers={"Accept": "application/json"},
                timeout=timeout_s,
            )
            r.raise_for_status()
            data = r.json()
            items: List[Dict[str, Any]] = []
            for el in data.get("elements", []):
                tags = el.get("tags", {}) or {}
                if "lat" not in el or "lon" not in el:
                    continue
                name = tags.get("name") or tags.get("operator") or "Unknown"
                addr = " ".join(
                    x for x in [
                        tags.get("addr:housenumber"),
                        tags.get("addr:street"),
                        tags.get("addr:suburb"),
                        tags.get("addr:city"),
                    ] if x
                ).strip()
                items.append({
                    "id": el.get("id"),
                    "osm_type": el.get("type"),
                    "name": name,
                    "lat": float(el["lat"]),
                    "lon": float(el["lon"]),
                    "address": addr if addr else None,
                    "phone": tags.get("phone") or tags.get("contact:phone"),
                    "website": tags.get("website") or tags.get("contact:website"),
                    "opening_hours": tags.get("opening_hours"),
                    "tags": tags,
                })
            return items
        except Exception as e:
            last_err = e
            continue
    if last_err:
        raise last_err
    return []
