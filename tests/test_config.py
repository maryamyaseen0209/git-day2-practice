def test_config_does_not_expose_api_key(client):
    """Test config endpoint doesn't leak sensitive information"""
    response = client.get("/config")
    assert response.status_code == 200
    
    data = response.json()
    
    # Verify expected fields exist
    assert "app_name" in data
    assert "environment" in data
    
    # Verify sensitive data is NOT exposed
    assert "api_key" not in data