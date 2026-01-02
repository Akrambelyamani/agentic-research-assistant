from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_requires_location():
    r = client.get("/api/search?type=pharmacy&radius=1000&limit=5")
    assert r.status_code == 400
