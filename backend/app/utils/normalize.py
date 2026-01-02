from typing import Any, Dict

def normalize_place(el: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert Overpass element to a normalized dict for ranking and API response.
    Overpass may return:
      - node with lat/lon
      - way/relation with center {lat, lon}
    """
    tags = el.get("tags") or {}
    name = tags.get("name") or tags.get("operator") or "(unnamed)"
    address_parts = []
    for k in ["addr:street", "addr:housenumber", "addr:suburb", "addr:city"]:
        if tags.get(k):
            address_parts.append(str(tags[k]))
    address = ", ".join(address_parts) if address_parts else None

    lat = el.get("lat")
    lon = el.get("lon")
    if lat is None or lon is None:
        center = el.get("center") or {}
        lat = center.get("lat")
        lon = center.get("lon")

    # stable id
    el_id = f"{el.get('type','x')}:{el.get('id','0')}"

    # Keep only useful tags (but preserve all in `tags` for details)
    return {
        "id": el_id,
        "name": str(name),
        "lat": lat,
        "lon": lon,
        "address": address,
        "tags": tags,
    }
