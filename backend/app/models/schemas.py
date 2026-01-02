from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class SearchResponseItem(BaseModel):
    id: Optional[int] = None
    osm_type: Optional[str] = None
    name: str
    lat: float
    lon: float
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    opening_hours: Optional[str] = None
    distance_m: Optional[int] = None
    tags: Dict[str, Any] = Field(default_factory=dict)

class SearchResponse(BaseModel):
    run_id: str
    query: str
    place_type: str
    radius_m: int
    count: int
    center: Dict[str, float]
    triage_hint: str
    items: List[SearchResponseItem]
    timings_ms: Dict[str, int] = Field(default_factory=dict)
    providers: Dict[str, str] = Field(default_factory=dict)
