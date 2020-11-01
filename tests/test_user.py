import json


def test_dont_store_user_passwords(user_predictable_password) -> None:
    assert user_predictable_password.password != "password"
    assert user_predictable_password.check_password("password")


# TODO: paramaterize some of these tests
def test_users_get(client, session_token, helpers) -> None:
    headers = helpers.headers(session_token)
    response = client.get(
        "/api/v1/users",
        headers=headers,
    )

    helpers.assert_success(response)

    assert isinstance(response.json, list)
    assert len(response.json) > 0

    first_element = response.json[0]
    assert first_element["username"] == "admin"
    assert isinstance(first_element["roles"], list)
    assert "password" not in first_element


def test_users_post(client, session_token, helpers) -> None:
    headers = helpers.headers(session_token)
    response = client.post(
        "/api/v1/users",
        data=json.dumps({"username": "testuser1", "password": "reallygoodpassword"}),
        headers=headers,
    )

    helpers.assert_success(response)


def test_user_get(client, session_token, helpers, user) -> None:
    headers = helpers.headers(session_token)
    response = client.get(
        f"/api/v1/users/{user.id}",
        headers=headers,
    )

    helpers.assert_success(response)


def test_user_put(client, session_token, helpers, user) -> None:
    headers = helpers.headers(session_token)
    response = client.put(
        f"/api/v1/users/{user.id}",
        headers=headers,
        data=json.dumps({"username": user.username, "password": "changedpassword"}),
    )

    helpers.assert_success(response)


def test_user_delete(client, session_token, helpers, user) -> None:
    headers = helpers.headers(session_token)
    response = client.delete(f"/api/v1/users/{user.id}", headers=headers)

    helpers.assert_success(response)
