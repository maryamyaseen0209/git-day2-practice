from fastapi.testclient import TestClient
from your_package_name.api import app

client = TestClient(app)

def test_basic_health_exists() -> None:
    response = client.get("/health")
    assert response.status_code == 200

def test_readiness_endpoint_exists() -> None:
    response = client.get("/health/ready")
    # May fail if deps not available in test env, but endpoint should exist
    assert response.status_code in [200, 503]
