import requests
import pytest
from unittest.mock import Mock
from custom_components.dimo.dimoapi import DimoClient, Auth
from custom_components.dimo.dimoapi.auth import (
    InvalidApiKeyFormat,
    InvalidClientIdError,
    InvalidCredentialsError,
)


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
        auth.token, privileges=[1, 2, 3, 4], token_id=vehicle_token_id
    )


@pytest.mark.parametrize(
    "mocked_exception,expected_exception",
    [
        (requests.exceptions.HTTPError("404"), InvalidClientIdError),
        (requests.exceptions.HTTPError("400"), InvalidCredentialsError),
        (ValueError("Invalid API key format"), InvalidApiKeyFormat),
    ],
)
def test_auth_exceptions(mocker, mocked_exception, expected_exception):
    dimo_mock = Mock()
    dimo_mock.auth.get_token = Mock(side_effect=mocked_exception)

    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)

    with pytest.raises(expected_exception):
        auth.get_token()
