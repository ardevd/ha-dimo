from unittest.mock import Mock

import dimo as dimo_sdk
import pytest

from custom_components.dimo.dimoapi import Auth, DimoClient
from custom_components.dimo.dimoapi.auth import (InvalidApiKeyFormat,
                                                 InvalidClientIdError,
                                                 InvalidCredentialsError)

from .helper import create_mock_token


def test_auth_get_token(mocker):
    fake_token = create_mock_token(3600)
    # Mocking the DIMO instance and auth.get_token
    dimo_mock = Mock()

    dimo_mock.auth.get_dev_jwt = Mock(return_value={"access_token": fake_token.token})
    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)

    # Test token retrieval
    token = auth.get_access_token()

    assert token == fake_token
    dimo_mock.auth.get_dev_jwt.assert_called_once_with(
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
    auth.access_token = fake_token  # Simulate an already set token

    # Ensure that get_token does not call _get_auth if token is already set
    token = auth.get_access_token()

    assert token == fake_token
    dimo_mock.auth.get_token.assert_not_called()


def test_auth_get_dimo():
    dimo_mock = Mock()
    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)

    assert auth.get_dimo() == dimo_mock


def test_auth_get_token_calls_get_auth_when_token_is_none(mocker):
    fake_token = create_mock_token(3600)  # 1 hour from now
    dimo_mock = Mock()
    dimo_mock.auth.get_dev_jwt = Mock(return_value={"access_token": fake_token.token})

    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)

    token = auth.get_access_token()

    assert token == fake_token
    dimo_mock.auth.get_dev_jwt.assert_called_once_with(
        client_id="client_id", domain="domain", private_key="private_key"
    )


def test_auth_get_privileged_token(mocker):
    fake_privileged_token = create_mock_token(1600)
    fake_response = {"token": fake_privileged_token.token}
    vehicle_token_id = "1337"

    # Mock DIMO instance and token_exchange
    dimo_mock = Mock()
    dimo_mock.token_exchange.exchange = Mock(return_value=fake_response)

    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)
    auth.access_token = create_mock_token(3600)

    # Test privileged token retrieval
    privileged_token = auth.get_privileged_token(vehicle_token_id)

    assert privileged_token.token == fake_privileged_token.token
    dimo_mock.token_exchange.exchange.assert_called_once_with(
        developer_jwt=auth.access_token.token,
        token_id=vehicle_token_id,
    )


def test_auth_get_privileged_token_without_permissions(mocker):
    fake_privileged_token = create_mock_token(1600)
    fake_response = {"token": fake_privileged_token.token}
    vehicle_token_id = "1337"

    # Mock DIMO instance and token_exchange
    dimo_mock = Mock()
    dimo_mock.token_exchange.exchange = Mock(return_value=fake_response)

    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)
    auth.access_token = create_mock_token(3600)

    # Test privileged token retrieval
    privileged_token = auth.get_privileged_token(vehicle_token_id)

    assert privileged_token.token == fake_privileged_token.token
    dimo_mock.token_exchange.exchange.assert_called_once_with(
        developer_jwt=auth.access_token.token,
        token_id=vehicle_token_id,
    )


@pytest.mark.parametrize(
    "mocked_exception,expected_exception",
    [
        (
            dimo_sdk.request.HTTPError(status=404, message="Invalid Client ID"),
            InvalidClientIdError,
        ),
        (
            dimo_sdk.request.HTTPError(status=400, message="Invalid credentials error"),
            InvalidCredentialsError,
        ),
        (ValueError("Invalid API key format"), InvalidApiKeyFormat),
    ],
)
def test_auth_exceptions(mocker, mocked_exception, expected_exception):
    dimo_mock = Mock()
    dimo_mock.auth.get_dev_jwt = Mock(side_effect=mocked_exception)

    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)

    with pytest.raises(expected_exception):
        auth.get_access_token()


def test_is_privileged_token_not_expired(mocker):
    # Mock the instance and its privileged tokens
    auth_instance = Auth("client_id", "domain", "private_key")
    vehicle_token_id = "123"
    token = create_mock_token(600)  # Expires in 10 minutes

    auth_instance.privileged_tokens[vehicle_token_id] = token

    # Test the method
    assert not auth_instance.privileged_tokens[vehicle_token_id].is_expired()


def test_is_privileged_token_expired():
    # Create an instance of Auth
    auth_instance = Auth("client_id", "domain", "private_key")
    vehicle_token_id = "123"

    # Generate an expired token (expired 10 minutes ago)
    jwt_value = create_mock_token(-600)  # Negative offset indicates past expiry
    auth_instance.privileged_tokens[vehicle_token_id] = jwt_value

    # Assert the token is recognized as expired
    assert auth_instance.privileged_tokens[vehicle_token_id].is_expired


def test_access_token_not_refreshed_if_not_expired(mocker):
    """Ensures we don't refresh the access token if it's still valid."""
    dimo_mock = Mock()
    # Make sure if we do fetch, it would be some placeholder
    dimo_mock.auth.get_dev_jwt = Mock(return_value={"access_token": "unused_new_token"})

    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)
    valid_token = create_mock_token(3600)  # 1 hour from now
    auth.access_token = valid_token

    # This call should NOT trigger a refresh
    token = auth.get_access_token()

    assert token == valid_token
    dimo_mock.auth.get_dev_jwt.assert_not_called()
