from unittest.mock import Mock
from custom_components.dimo.dimoapi import DimoClient


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


def test_dimo_client_get_latest_signals():
    auth_mock = Mock()
    dimo_mock = Mock()
    priv_token = {"token": "privileged_token_123"}
    auth_mock.get_privileged_token.return_value = priv_token

    dimo_client = DimoClient(auth=auth_mock)
    dimo_client.dimo = dimo_mock  # Inject the dimo mock

    token_id = "123"
    signal_names = ["speed", "batteryLevel"]
    query_result = {
        "signalsLatest": {
            "speed": {"timestamp": "2024-11-27T12:00:00Z", "value": 60},
            "batteryLevel": {"timestamp": "2024-11-27T12:00:00Z", "value": 80},
        }
    }
    dimo_mock.telemetry.query.return_value = query_result

    result = dimo_client.get_latest_signals(token_id, signal_names)

    # Assert the result matches the query result
    assert result == query_result

    # Assert the query was constructed correctly
    expected_query = f"""
        query {{
            signalsLatest(tokenId: {token_id}) {{
                speed {{
                  timestamp
                  value
                }}
                batteryLevel {{
                  timestamp
                  value
                }}
            }}
        }}
    """

    # Normalize whitespace for comparison
    actual_query = dimo_mock.telemetry.query.call_args[0][0]  # Get the actual query
    assert "".join(actual_query.split()) == "".join(
        expected_query.split()
    ), f"Query mismatch.\nExpected:\n{expected_query}\nActual:\n{actual_query}"

    # Ensure privileged token was used
    dimo_mock.telemetry.query.assert_called_once_with(actual_query, priv_token["token"])
    auth_mock.get_privileged_token.assert_called_once_with(token_id)
