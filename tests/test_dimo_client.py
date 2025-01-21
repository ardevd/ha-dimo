from .helper import create_mock_token
from unittest.mock import Mock
from custom_components.dimo.dimoapi import DimoClient


def test_dimo_client_init():
    # Arrange: Set up mocks
    auth_mock = Mock()
    dimo_client = DimoClient(auth=auth_mock)

    # Act: Call the method under test
    dimo_client.init()

    # Assert: Verify interactions
    auth_mock.get_access_token.assert_called_once()


def test_dimo_client_get_vehicle_makes():
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    dimo_mock.device_definitions.list_device_makes.return_value = ["Ford", "Tesla"]

    dimo_client = DimoClient(auth=auth_mock)
    makes = dimo_client.get_vehicle_makes()

    # Assert the result
    assert makes == ["Ford", "Tesla"]
    dimo_mock.device_definitions.list_device_makes.assert_called_once()


def test_dimo_client_get_rewards_for_vehicle():
    # Arrange: Set up mocks
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    dimo_client = DimoClient(auth=auth_mock)
    token_id = "vehicle123"

    # Mock the GraphQL query result
    query_result = {"data": {"vehicle": {"earnings": {"totalTokens": 100.5}}}}
    dimo_mock.identity.query.return_value = query_result

    # Act: Call the method under test
    result = dimo_client.get_rewards_for_vehicle(token_id)

    dimo_mock.identity.query.assert_called_once_with(
        f"""
query GetVehicleRewardsByTokenId {{
  vehicle(tokenId: {token_id}) {{
      earnings {{
        totalTokens
      }}
    }}
}}
"""
    )


def test_dimo_client_get_available_signals():
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    priv_token = create_mock_token(3600)
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
query AvailableSignals {{
  availableSignals(tokenId: {token_id})
}}
""",
        priv_token.token,
    )
    auth_mock.get_privileged_token.assert_called_once_with(token_id)


def test_dimo_client_get_latest_signals():
    auth_mock = Mock()
    dimo_mock = Mock()
    priv_token = create_mock_token(3600)
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
    dimo_mock.telemetry.query.assert_called_once_with(actual_query, priv_token.token)
    auth_mock.get_privileged_token.assert_called_once_with(token_id)


def test_dimo_client_get_vin_success():
    # Arrange: Set up mocks
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    dimo_client = DimoClient(auth=auth_mock)
    token_id = "vehicle123"

    # Mock the privileged token and VIN response
    mocked_token = create_mock_token(3600)
    auth_mock.get_privileged_token.return_value = mocked_token
    dimo_mock.telemetry.get_vin.return_value = {
        "data": {"vinVCLatest": {"vin": "1HGCM82633A123456"}}
    }

    # Act: Call the method under test
    vin = dimo_client.get_vin(token_id)

    # Assert: Verify the results and interactions
    assert vin == "1HGCM82633A123456"
    auth_mock.get_privileged_token.assert_called_once_with(token_id)
    dimo_mock.telemetry.get_vin.assert_called_once_with(mocked_token.token, token_id)


def test_dimo_client_get_vin_malformed_response():
    # Arrange: Set up mocks
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    dimo_client = DimoClient(auth=auth_mock)
    token_id = "vehicle123"

    # Mock the privileged token and malformed response
    mocked_token = create_mock_token(1200)
    auth_mock.get_privileged_token.return_value = mocked_token
    dimo_mock.telemetry.get_vin.return_value = {"unexpected_key": "unexpected_value"}

    # Act: Call the method under test
    vin = dimo_client.get_vin(token_id)

    # Assert: Verify the results and interactions
    assert vin is None
    auth_mock.get_privileged_token.assert_called_once_with(token_id)
    dimo_mock.telemetry.get_vin.assert_called_once_with(mocked_token.token, token_id)


def test_dimo_client_get_total_dimo_vehicles_success():
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    dimo_client = DimoClient(auth=auth_mock)

    dimo_mock.identity.count_dimo_vehicles.return_value = {
        "data": {"vehicles": {"totalCount": 1234}}
    }

    total_vehicles = dimo_client.get_total_dimo_vehicles()

    assert total_vehicles == 1234
    dimo_mock.identity.count_dimo_vehicles.assert_called_once()


def test_dimo_client_get_total_dimo_vehicles_exception():
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    dimo_client = DimoClient(auth=auth_mock)

    dimo_mock.identity.count_dimo_vehicles.side_effect = Exception("API error")

    total_vehicles = dimo_client.get_total_dimo_vehicles()

    assert total_vehicles is None
    dimo_mock.identity.count_dimo_vehicles.assert_called_once()
