from unittest.mock import Mock
from custom_components.dimo.dimoapi import DimoClient, Auth


def test_auth_get_token(mocker):
    fake_token = "abcdef1234"
    # Mocking the DIMO instance and auth.get_token
    dimo_mock = Mock()
    dimo_mock.auth.get_token = Mock(return_value={"access_token": fake_token})

    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)

    # Test token retrieval
    token = auth.get_token()

    assert token == fake_token
    dimo_mock.auth.get_token.assert_called_once_with(
        client_id="client_id", domain="domain", private_key="private_key"
    )


def test_dimo_client_get_vehicle_makes(mocker):
    # Mocking DIMO instance and list_device_makes
    dimo_mock = Mock()
    dimo_mock.device_definitions.list_device_makes = Mock(
        return_value=["Land Rover", "BMW"]
    )

    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)
    client = DimoClient(auth)

    # Test get_vehicle_makes
    makes = client.get_vehicle_makes()

    assert makes == ["Land Rover", "BMW"]
    dimo_mock.device_definitions.list_device_makes.assert_called_once()


def test_auth_token_caching(mocker):
    # Mock DIMO instance and auth.get_token
    fake_token = "cached_token"
    dimo_mock = Mock()
    dimo_mock.auth.get_token = Mock(return_value={"access_token": fake_token})

    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)
    auth.token = fake_token  # Simulate an already set token

    # Ensure that get_token does not call _get_auth if token is already set
    token = auth.get_token()

    assert token == fake_token
    dimo_mock.auth.get_token.assert_not_called()


def test_auth_get_dimo():
    dimo_mock = Mock()
    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)

    assert auth.get_dimo() == dimo_mock


def test_auth_get_token_calls_get_auth_when_token_is_none(mocker):
    fake_token = "new_token"
    dimo_mock = Mock()
    dimo_mock.auth.get_token = Mock(return_value={"access_token": fake_token})

    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)

    token = auth.get_token()

    assert token == fake_token
    dimo_mock.auth.get_token.assert_called_once_with(
        client_id="client_id", domain="domain", private_key="private_key"
    )


def test_auth_get_privileged_token(mocker):
    fake_privileged_token = "privileged_token_1234"
    vehicle_token_id = "1337"

    # Mock DIMO instance and token_exchange
    dimo_mock = Mock()
    dimo_mock.token_exchange.exchange = Mock(return_value=fake_privileged_token)

    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)
    auth.token = "current_token"

    # Test privileged token retrieval
    privileged_token = auth.get_privileged_token(vehicle_token_id)

    assert privileged_token == fake_privileged_token
    dimo_mock.token_exchange.exchange.assert_called_once_with(
        auth.token, privileges=[1, 3], token_id=vehicle_token_id
    )


def test_auth_invalid_client_id_error(mocker):
    dimo_mock = Mock()
    # Simulate HTTPError with 404
    mocker.patch(
        "requests.post",
        side_effect=requests.exceptions.HTTPError(
            "404 Client Error: Not Found for url: https://auth.dimo.zone/auth/web3/generate_challenge"
        ),
    )
    dimo_mock.auth.get_token = Mock(side_effect=requests.exceptions.HTTPError("404"))

    auth = Auth("invalid_client_id", "domain", "private_key", dimo=dimo_mock)

    with pytest.raises(Auth.InvalidClientIdError):
        auth.get_token()


def test_auth_invalid_credentials_error(mocker):
    dimo_mock = Mock()
    # Simulate HTTPError with 400
    dimo_mock.auth.get_token = Mock(side_effect=requests.exceptions.HTTPError("400"))

    auth = Auth("client_id", "domain", "invalid_private_key", dimo=dimo_mock)

    with pytest.raises(Auth.InvalidCredentialsError):
        auth.get_token()


def test_auth_invalid_api_key_format(mocker):
    dimo_mock = Mock()
    # Simulate ValueError
    dimo_mock.auth.get_token = Mock(
        side_effect=ValueError(
            "The private key must be exactly 32 bytes long, instead of 65 bytes"
        )
    )

    auth = Auth("client_id", "domain", "bad_key_format", dimo=dimo_mock)

    with pytest.raises(Auth.InvalidApiKeyFormat):
        auth.get_token()
