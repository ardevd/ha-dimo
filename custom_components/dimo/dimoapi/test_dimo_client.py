from unittest.mock import Mock
from dimo_client import DimoClient


def test_dimo_client_init():
    # Mock the Auth instance
    auth_mock = Mock()
    dimo_client = DimoClient(auth=auth_mock)

    # Check that DimoClient was initialized with the mocked auth
    assert dimo_client.auth == auth_mock
    assert dimo_client.dimo == auth_mock.get_dimo.return_value


def test_dimo_client_get_vehicle_makes():
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    dimo_mock.device_definitions.list_device_makes.return_value = ["Ford", "Tesla"]

    dimo_client = DimoClient(auth=auth_mock)
    makes = dimo_client.get_vehicle_makes()

    # Assert the result
    assert makes == ["Ford", "Tesla"]
    dimo_mock.device_definitions.list_device_makes.assert_called_once()


def test_dimo_client_get_available_signals():
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    priv_token = {"token": "privileged_token_123"}
    auth_mock.get_privileged_token.return_value = priv_token

    dimo_client = DimoClient(auth=auth_mock)
    token_id = "vehicle123"
    query_result = {"availableSignals": []}
    dimo_mock.telemetry.query.return_value = query_result

    result = dimo_client.get_available_signals(token_id)

    # Assert the result and query
    assert result == query_result
    dimo_mock.telemetry.query.assert_called_once_with(
        f"""
    query {{
      availableSignals(
        tokenId: {token_id}
      )
    }}
    """,
        priv_token["token"],
    )
    auth_mock.get_privileged_token.assert_called_once_with(token_id)
