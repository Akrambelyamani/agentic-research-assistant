from app.agents.health_locator_agent import HealthLocatorAgent

def test_validate_type():
    a = HealthLocatorAgent()
    assert a._validate_type("pharmacy") == "pharmacy"
    assert a._validate_type("HOSPITAL") == "hospital"
