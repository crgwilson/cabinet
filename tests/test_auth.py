from cabinet.auth.permissions import all_roles


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
