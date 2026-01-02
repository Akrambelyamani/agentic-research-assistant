from fastapi import APIRouter, Query, HTTPException
from typing import Literal
import math
import uuid

from app.core.config import settings
from app.services.geocoding import geocode_query
from app.services.overpass_client import search_nearby_places

router = APIRouter(prefix="/api", tags=["search"])


@router.get("/search")
def search(
    q: str = Query(..., description="City or district"),
    type: Literal["pharmacy", "hospital"] = "pharmacy",
    radius: int = Query(1200, ge=200, le=5000),
    limit: int = Query(12, ge=1, le=50),
):
    """
    Search nearby health facilities using OpenStreetMap.
    """

    # 1) Geocoding
    coords = geocode_query(
        query=q,
        nominatim_url=settings.NOMINATIM_URL,
        user_agent=settings.USER_AGENT,
    )
    if not coords:
        raise HTTPException(status_code=404, detail="Location not found")

    lat, lon = coords

    # 2) Overpass search
    try:
        items = search_nearby_places(
            lat=lat,
            lon=lon,
            radius_m=radius,
            place_type=type,
            limit=limit,
            overpass_url=settings.OVERPASS_URL,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Overpass error: {e}")

    # 3) Distance calc (Haversine)
    def dist_m(a, b, c, d):
        R = 6371000
        phi1, phi2 = math.radians(a), math.radians(c)
        dphi = math.radians(c - a)
        dl = math.radians(d - b)
        x = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dl / 2) ** 2
        return int(2 * R * math.asin(math.sqrt(x)))

    for it in items:
        it["distance_m"] = dist_m(lat, lon, it["lat"], it["lon"])

    items.sort(key=lambda x: x["distance_m"])

    # 4) Response
    return {
        "run_id": uuid.uuid4().hex[:8],
        "query": q,
        "place_type": type,
        "radius_m": radius,
        "count": len(items),
        "center": {"lat": lat, "lon": lon},
        "items": items,
    }
