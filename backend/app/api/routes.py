from fastapi import APIRouter, Query
from app.agents.health_locator_agent import HealthLocatorAgent
from app.models.schemas import SearchResponse

router = APIRouter()
agent = HealthLocatorAgent()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(..., min_length=2),
    type: str = Query("pharmacy"),
    radius: int = Query(2000, ge=50, le=50000),
    limit: int = Query(20, ge=1, le=100),
):
    return agent.run(q=q, place_type=type, radius_m=radius, limit=limit)
