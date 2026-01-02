import hashlib
import json
import os
import time
from typing import Any, Optional

def _key_to_path(cache_dir: str, key: str) -> str:
    os.makedirs(cache_dir, exist_ok=True)
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]
    return os.path.join(cache_dir, f"{digest}.json")

def cache_get(cache_dir: str, key: str, ttl_s: int) -> Optional[Any]:
    path = _key_to_path(cache_dir, key)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        ts = float(payload.get("_ts", 0))
        if ttl_s > 0 and (time.time() - ts) > ttl_s:
            return None
        return payload.get("value")
    except Exception:
        return None

def cache_set(cache_dir: str, key: str, value: Any) -> None:
    path = _key_to_path(cache_dir, key)
    payload = {"_ts": time.time(), "value": value}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
