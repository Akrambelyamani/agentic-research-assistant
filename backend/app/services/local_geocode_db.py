from typing import Optional, Tuple

_DB = {
    "casablanca": (33.57311, -7.589843),
    "casablanca maarif": (33.5909, -7.6363),
    "maarif": (33.5909, -7.6363),
    "rabat": (34.020882, -6.84165),
    "tanger": (35.759465, -5.833954),
    "fes": (34.033333, -5.0),
    "marrakech": (31.629472, -7.981084),
    "agadir": (30.427755, -9.598107),
}

def local_geocode(query: str) -> Optional[Tuple[float, float]]:
    q = (query or "").strip().lower()
    if not q:
        return None
    return _DB.get(q)
