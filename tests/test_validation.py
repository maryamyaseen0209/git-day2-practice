def test_create_item_validation_error_returns_400(client):
    """Test validation errors return 400 with proper error format"""
    # Invalid payload: empty name + negative price
    payload = {"name": "", "price": -1, "in_stock": True}

    response = client.post("/items", json=payload)

    assert response.status_code == 400
    body = response.json()
    assert body["error_type"] == "validation_error"
