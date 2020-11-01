import json

import pytest

from tests.constants import API_TEST_CASES


def test_cls_dont_store_user_passwords(user_predictable_password) -> None:
    assert user_predictable_password.password != "password"
    assert user_predictable_password.check_password("password")


@pytest.mark.parametrize(
    "case,expected_status_code",
    API_TEST_CASES,
)
def test_api_users_get(client, headers, case, expected_status_code) -> None:
    response = client.get(
        "/api/v1/users",
        headers=headers[case],
    )
    assert response.status_code == expected_status_code

    # Test response if we were expecting a success
    if response.status_code == 200:
        assert isinstance(response.json, list)
        assert len(response.json) > 0

        first_element = response.json[0]
        assert first_element["username"] == "admin"
        assert isinstance(first_element["roles"], list)
        assert "password" not in first_element


@pytest.mark.parametrize(
    "case,expected_status_code",
    API_TEST_CASES,
)
def test_api_users_post(client, headers, case, expected_status_code) -> None:
    response = client.post(
        "/api/v1/users",
        data=json.dumps({"username": "testuser1", "password": "reallygoodpassword"}),
        headers=headers[case],
    )

    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "case,expected_status_code",
    API_TEST_CASES,
)
def test_api_user_get(client, headers, user, case, expected_status_code) -> None:
    response = client.get(
        f"/api/v1/users/{user.id}",
        headers=headers[case],
    )

    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "case,expected_status_code",
    API_TEST_CASES,
)
def test_api_user_put(client, headers, user, case, expected_status_code) -> None:
    response = client.put(
        f"/api/v1/users/{user.id}",
        headers=headers[case],
        data=json.dumps({"username": user.username, "password": "changedpassword"}),
    )

    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "case,expected_status_code",
    API_TEST_CASES,
)
def test_api_user_delete(client, headers, user, case, expected_status_code) -> None:
    response = client.delete(f"/api/v1/users/{user.id}", headers=headers[case])

    assert response.status_code == expected_status_code
