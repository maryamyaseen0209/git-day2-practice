def test_secure_data_401_without_key(client):
    """Test secure endpoint returns 401 when no API key provided"""
    response = client.get("/secure-data")
    assert response.status_code == 401


def test_secure_data_200_with_key(client):
    """Test secure endpoint returns 200 with valid API key"""
    response = client.get("/secure-data", headers={"X-API-Key": "test-key"})
    assert response.status_code == 200
    assert response.json()["secret_data"] == "approved"
