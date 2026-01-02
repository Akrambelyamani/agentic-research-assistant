import math
import time
import uuid
from typing import Any, Dict, List

import requests
from fastapi import HTTPException

from app.core.config import settings
from app.services.geocoding import geocode_query
from app.services.overpass_client import overpass_search
from app.agents.safety_rules import triage_hint

def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dl / 2) ** 2
    return int(2 * R * math.asin(math.sqrt(a)))

class HealthLocatorAgent:
    def run(self, q: str, place_type: str, radius_m: int, limit: int) -> Dict[str, Any]:
        run_id = uuid.uuid4().hex[:8]
        timings: Dict[str, int] = {}
        providers: Dict[str, str] = {}

        t0 = time.time()
        try:
            coords = geocode_query(
                query=q,
                openmeteo_url=settings.OPENMETEO_GEOCODE_URL,
                nominatim_url=settings.NOMINATIM_URL,
                user_agent=settings.USER_AGENT,
                email=settings.NOMINATIM_EMAIL,
                timeout_s=settings.GEOCODE_TIMEOUT_S,
                retries=settings.GEOCODE_RETRIES,
                cache_dir=f"{settings.RUNS_DIR}/cache_geocode",
                cache_ttl_s=settings.GEOCODE_CACHE_TTL_S,
            )
        except requests.exceptions.ReadTimeout:
            coords = None
        except Exception:
            coords = None

        timings["geocode"] = int((time.time() - t0) * 1000)
        providers["geocode"] = "direct/local->open-meteo->nominatim"

        if not coords:
            raise HTTPException(
                status_code=400,
                detail="Geocoding unavailable on this network. Use 'q' as 'lat,lon' (example: 33.5731,-7.5898) or a supported local name (e.g., Casablanca, Casablanca Maarif).",
            )

        lat, lon = coords

        overpass_urls = [u.strip() for u in settings.OVERPASS_URLS.split(",") if u.strip()]
        last_err: Exception | None = None
        items: List[Dict[str, Any]] = []

        t1 = time.time()
        for u in overpass_urls:
            try:
                items = overpass_search(
                    lat=lat,
                    lon=lon,
                    radius_m=radius_m,
                    place_type=place_type,
                    limit=limit,
                    overpass_url=u,
                    timeout_s=settings.OVERPASS_TIMEOUT_S,
                    retries=settings.OVERPASS_RETRIES,
                )
                providers["overpass"] = u
                last_err = None
                break
            except Exception as e:
                last_err = e
                continue

        timings["overpass"] = int((time.time() - t1) * 1000)

        if last_err and not items:
            if isinstance(last_err, requests.exceptions.ReadTimeout):
                raise HTTPException(status_code=504, detail="Overpass timeout. Try again.")
            raise HTTPException(status_code=502, detail=f"Overpass error: {last_err}")

        for it in items:
            it["distance_m"] = haversine_m(lat, lon, it["lat"], it["lon"])
        items.sort(key=lambda x: x.get("distance_m", 10**12))

        return {
            "run_id": run_id,
            "query": q,
            "place_type": place_type,
            "radius_m": radius_m,
            "count": len(items),
            "center": {"lat": lat, "lon": lon},
            "triage_hint": triage_hint(place_type=place_type, count=len(items), radius_m=radius_m),
            "items": items[: max(1, int(limit))],
            "timings_ms": timings,
            "providers": providers,
        }
