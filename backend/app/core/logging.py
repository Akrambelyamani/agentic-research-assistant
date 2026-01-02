from pathlib import Path
import json
from datetime import datetime, timezone
from typing import Any, Dict

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def write_md(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
