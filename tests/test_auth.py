from cabinet.auth.controllers import AuthToken, get_all_user_permissions, has_permission
from cabinet.auth.permissions import ApiPermission, all_roles


def test_roles_get(client, helpers) -> None:
    response = client.get("/api/v1/roles")

    helpers.assert_success(response)

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


def test_token_encode(now) -> None:
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


def test_get_all_user_permissions(user) -> None:
    all_permissions = get_all_user_permissions(user.id)

    for role in user.roles:
        for permission in role.permissions:
            assert permission in all_permissions


def test_has_permission_admin_user(admin_user) -> None:
    user_permission = ApiPermission(object="User", read=True, write=False)
    assert has_permission(admin_user.id, user_permission)


def test_has_permission_normal_user(user) -> None:
    user_permission = ApiPermission(object="User", read=True, write=False)
    assert not has_permission(user.id, user_permission)
