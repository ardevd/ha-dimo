import jwt
import requests
from datetime import datetime, timedelta, timezone
import pytest
from unittest.mock import Mock
from custom_components.dimo.dimoapi import DimoClient, Auth
from custom_components.dimo.dimoapi.auth import (
    PrivilegedToken,
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
    fake_token = create_mock_token(3600)
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
    fake_token = create_mock_token(3600)  # 1 hour from now
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
    fake_response = {"token": fake_privileged_token}
    vehicle_token_id = "1337"

    # Mock DIMO instance and token_exchange
    dimo_mock = Mock()
    dimo_mock.token_exchange.exchange = Mock(return_value=fake_response)

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


def create_mock_token(exp_offset):
    """
    Helper function to create a mock JWT token with a specific expiration offset.
    """
    expiration_time = datetime.now(timezone.utc) + timedelta(seconds=exp_offset)
    payload = {"exp": expiration_time.timestamp()}
    return jwt.encode(payload, "secret", algorithm="HS256")


def test_is_privileged_token_not_expired(mocker):
    # Mock the instance and its privileged tokens
    auth_instance = Auth("client_id", "domain", "private_key")
    vehicle_token_id = "123"
    token = create_mock_token(600)  # Expires in 10 minutes

    auth_instance.privileged_tokens[vehicle_token_id] = PrivilegedToken(token)

    # Test the method
    assert not auth_instance._is_privileged_token_expired(vehicle_token_id)


def test_is_privileged_token_expired():
    # Create an instance of Auth
    auth_instance = Auth("client_id", "domain", "private_key")
    vehicle_token_id = "123"

    # Generate an expired token (expired 10 minutes ago)
    jwt_value = create_mock_token(-600)  # Negative offset indicates past expiry
    auth_instance.privileged_tokens[vehicle_token_id] = PrivilegedToken(jwt_value)

    # Assert the token is recognized as expired
    assert auth_instance._is_privileged_token_expired(vehicle_token_id)


def test_main_token_not_refreshed_if_not_expired(mocker):
    """Ensures we don't refresh the main token if it's still valid."""
    dimo_mock = Mock()
    # Make sure if we do fetch, it would be some placeholder
    dimo_mock.auth.get_token = Mock(return_value={"access_token": "unused_new_token"})

    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)
    valid_token = create_mock_token(3600)  # 1 hour from now
    auth.token = valid_token

    # This call should NOT trigger a refresh
    token = auth.get_token()

    assert token == valid_token
    dimo_mock.auth.get_token.assert_not_called()
