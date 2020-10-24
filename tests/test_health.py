def test_health_get(client, helpers):
    response = client.get("/api/v1/health")

    helpers.assert_success(response)
