import json


def test_users_get(client, helpers) -> None:
    response = client.get("/api/v1/users")

    helpers.assert_success(response)

    assert isinstance(response.json, list)
    assert len(response.json) > 0

    first_element = response.json[0]
    assert first_element["username"] == "admin"
    assert "password" not in first_element


def test_users_post(client, helpers) -> None:
    response = client.post(
        "/api/v1/users",
        data=json.dumps({"username": "testuser1", "password": "reallygoodpassword"}),
        content_type=helpers.CONTENT_TYPE,
    )

    helpers.assert_success(response)
