from typing import Any, Dict, List
from ..utils.distance import haversine_m

def rank_and_filter(center_lat: float, center_lon: float, items: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    cleaned: List[Dict[str, Any]] = []
    seen = set()

    for it in items:
        lat = it.get("lat")
        lon = it.get("lon")
        if lat is None or lon is None:
            continue

        # Deduplicate by (name, rounded coords)
        key = (it.get("name","").strip().lower(), round(float(lat), 5), round(float(lon), 5))
        if key in seen:
            continue
        seen.add(key)

        dist = haversine_m(center_lat, center_lon, float(lat), float(lon))
        it["distance_m"] = int(dist)
        cleaned.append(it)

    # Sort by distance
    cleaned.sort(key=lambda x: x.get("distance_m", 10**9))

    # Keep top
    return cleaned[:limit]
