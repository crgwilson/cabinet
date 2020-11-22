import json

import pytest

from cabinet.auth.controllers import AuthToken, get_all_user_permissions, has_permission
from cabinet.auth.permissions import ApiPermission, all_roles

from tests.constants import API_TEST_CASES


@pytest.mark.parametrize(
    "use_real_user,use_real_password,expected_status_code",
    [
        (True, True, 200),
        (True, False, 401),
        (False, True, 401),
        (False, False, 401),
    ],
)
def test_api_login_post(
    use_real_user,
    use_real_password,
    expected_status_code,
    client,
    headers,
    user_predictable_password,
) -> None:
    real_username = user_predictable_password.username
    real_password = "password"

    fake_username = "this_is_a_fake_username"
    fake_password = "this_is_a_fake_password"

    if use_real_user:
        username = real_username
    else:
        username = fake_username

    if use_real_password:
        password = real_password
    else:
        password = fake_password

    response = client.post(
        "/api/v1/login",
        data=json.dumps({"username": username, "password": password}),
        headers=headers["no_auth"],
    )

    assert response.status_code == expected_status_code

    if response.status_code == 200:
        assert "token" in response.json

        token = response.json["token"]
        assert isinstance(token, str)


@pytest.mark.parametrize(
    "case,expected_status_code",
    API_TEST_CASES,
)
def test_api_roles_get(client, headers, case, expected_status_code) -> None:
    response = client.get("/api/v1/roles", headers=headers[case])

    assert response.status_code == expected_status_code

    if response.status_code == 200:
        json_response = response.json
        assert isinstance(json_response, list)
        assert len(json_response) == 1

        for i in range(len(json_response)):
            response_obj = json_response[i]
            reference_obj = all_roles[i]

            expected_id = i + 1

            assert response_obj["id"] == expected_id
            assert response_obj["name"] == reference_obj.name
            assert response_obj["description"] == reference_obj.description


def test_cls_auth_token(now) -> None:
    mock_id = 14
    mock_dattime = now
    mock_ttl = 600
    mock_secret = "unittest"

    starting_token = AuthToken(mock_id, mock_dattime, mock_ttl, mock_secret)
    encoded_token = starting_token.encode()

    assert isinstance(encoded_token, bytes)

    decoded_token = AuthToken.decode(encoded_token, mock_secret)
    assert decoded_token.user_id == mock_id
    assert decoded_token.created_on == mock_dattime
    assert decoded_token.ttl == mock_ttl
    assert decoded_token.secret == mock_secret


def test_fn_get_all_user_permissions(user) -> None:
    all_permissions = get_all_user_permissions(user.id)

    for role in user.roles:
        for permission in role.permissions:
            assert permission in all_permissions


def test_fn_has_permission_admin_user(admin_user) -> None:
    user_permission = ApiPermission(object="User", read=True, write=False, delete=False)
    assert has_permission(admin_user.id, user_permission)


def test_fn_has_permission_normal_user(user) -> None:
    user_permission = ApiPermission(object="User", read=True, write=False, delete=False)
    assert not has_permission(user.id, user_permission)
