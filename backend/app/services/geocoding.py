from typing import Optional, Tuple
import requests
from app.services.cache import cache_get, cache_set
from app.services.local_geocode_db import local_geocode

def _parse_latlon(q: str) -> Optional[Tuple[float, float]]:
    s = (q or "").strip()
    if "," not in s:
        return None
    a, b = [x.strip() for x in s.split(",", 1)]
    try:
        lat = float(a)
        lon = float(b)
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return lat, lon
        return None
    except Exception:
        return None

def _openmeteo_geocode(query: str, url: str, timeout_s: int) -> Optional[Tuple[float, float]]:
    params = {"name": query, "count": 1, "language": "en", "format": "json"}
    r = requests.get(url, params=params, timeout=timeout_s)
    r.raise_for_status()
    data = r.json()
    results = data.get("results") or []
    if not results:
        return None
    return float(results[0]["latitude"]), float(results[0]["longitude"])

def _nominatim_geocode(query: str, url: str, user_agent: str, email: str, timeout_s: int) -> Optional[Tuple[float, float]]:
    headers = {"User-Agent": user_agent, "Accept": "application/json"}
    params = {"q": query, "format": "json", "limit": 1, "email": email}
    r = requests.get(url, params=params, headers=headers, timeout=timeout_s)
    r.raise_for_status()
    data = r.json()
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"])

def geocode_query(
    query: str,
    openmeteo_url: str,
    nominatim_url: str,
    user_agent: str,
    email: str,
    timeout_s: int,
    retries: int,
    cache_dir: str,
    cache_ttl_s: int,
) -> Optional[Tuple[float, float]]:
    q = (query or "").strip()
    if not q:
        return None

    direct = _parse_latlon(q)
    if direct:
        return direct

    local = local_geocode(q)
    if local:
        return local

    cache_key = f"geocode::{q.lower()}"
    cached = cache_get(cache_dir, cache_key, ttl_s=cache_ttl_s)
    if cached and isinstance(cached, list) and len(cached) == 2:
        return float(cached[0]), float(cached[1])

    last_err: Exception | None = None

    for _ in range(max(1, retries + 1)):
        try:
            coords = _openmeteo_geocode(q, openmeteo_url, timeout_s)
            if coords:
                cache_set(cache_dir, cache_key, [coords[0], coords[1]])
                return coords
            break
        except Exception as e:
            last_err = e

    for _ in range(max(1, retries + 1)):
        try:
            coords = _nominatim_geocode(q, nominatim_url, user_agent, email, timeout_s)
            if coords:
                cache_set(cache_dir, cache_key, [coords[0], coords[1]])
                return coords
            return None
        except Exception as e:
            last_err = e

    if last_err:
        raise last_err
    return None
