def test_health_get(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
