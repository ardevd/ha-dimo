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
    token_id = "75948"

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
    token_id = "75123"
    query_result = {"availableSignals": []}
    dimo_mock.telemetry.available_signals.return_value = query_result

    result = dimo_client.get_available_signals(token_id)

    # Assert the result and query
    assert result == query_result
    dimo_mock.telemetry.available_signals.assert_called_once_with(
        priv_token.token,
        token_id,
    )
    auth_mock.get_privileged_token.assert_called_once_with(token_id)


def test_dimo_client_get_latest_signals():
    auth_mock = Mock()
    dimo_mock = Mock()
    priv_token = create_mock_token(3600)
    auth_mock.get_privileged_token.return_value = priv_token

    dimo_client = DimoClient(auth=auth_mock)
    dimo_client.dimo = dimo_mock  # Inject the dimo mock

    token_id = "88888"
    signal_names = [
        "chassisAxleRow1WheelLeftTirePressure",
        "chassisAxleRow1WheelRightTirePressure",
        "chassisAxleRow2WheelLeftTirePressure",
        "chassisAxleRow2WheelRightTirePressure",
        "currentLocationAltitude",
        "currentLocationHeading",
        "currentLocationIsRedacted",
        "currentLocationLatitude",
        "currentLocationLongitude",
        "dimoAftermarketHDOP",
        "dimoAftermarketNSAT",
        "exteriorAirTemperature",
        "lowVoltageBatteryCurrentVoltage",
        "obdBarometricPressure",
        "obdDTCList",
        "obdDistanceWithMIL",
        "obdEngineLoad",
        "obdIntakeTemp",
        "obdMAP",
        "obdRunTime",
        "obdStatusDTCCount",
        "powertrainCombustionEngineECT",
        "powertrainCombustionEngineMAF",
        "powertrainCombustionEngineSpeed",
        "powertrainCombustionEngineTPS",
        "powertrainFuelSystemAbsoluteLevel",
        "powertrainFuelSystemRelativeLevel",
        "powertrainRange",
        "powertrainTractionBatteryChargingIsCharging",
        "powertrainTractionBatteryRange",
        "powertrainTractionBatteryStateOfChargeCurrent",
        "powertrainTransmissionTravelledDistance",
        "powertrainType",
        "speed",
    ]
    query_result = {
        "data": {
            "signalsLatest": {
                "chassisAxleRow1WheelLeftTirePressure": {
                    "timestamp": "2024-07-19T16:45:16.517921Z",
                    "value": 252.5,
                },
                "chassisAxleRow1WheelRightTirePressure": {
                    "timestamp": "2024-07-19T16:45:16.517921Z",
                    "value": 255.2,
                },
                "chassisAxleRow2WheelLeftTirePressure": {
                    "timestamp": "2024-07-19T16:45:16.517921Z",
                    "value": 293.7,
                },
                "chassisAxleRow2WheelRightTirePressure": {
                    "timestamp": "2024-07-19T16:45:16.517921Z",
                    "value": 296.4,
                },
                "dimoAftermarketHDOP": {
                    "timestamp": "2025-08-08T18:48:44Z",
                    "value": 0.8,
                },
                "dimoAftermarketNSAT": {
                    "timestamp": "2025-08-08T18:48:44Z",
                    "value": 22,
                },
                "exteriorAirTemperature": {
                    "timestamp": "2025-08-08T18:48:44Z",
                    "value": 18,
                },
                "lowVoltageBatteryCurrentVoltage": {
                    "timestamp": "2025-08-08T18:48:44Z",
                    "value": 12.786,
                },
                "obdBarometricPressure": {
                    "timestamp": "2024-12-02T07:25:42Z",
                    "value": 99,
                },
                "obdDTCList": {
                    "timestamp": "2025-08-08T18:48:47Z",
                    "obdDistanceWithMIL": {
                        "timestamp": "2025-08-08T18:48:44Z",
                        "value": 0,
                    },
                    "obdEngineLoad": {
                        "timestamp": "2024-11-28T19:13:38Z",
                        "value": 0.071,
                    },
                    "obdIntakeTemp": {"timestamp": "2024-12-02T07:28:11Z", "value": 18},
                    "obdMAP": {"timestamp": "2024-12-02T07:28:11Z", "value": 100},
                    "obdRunTime": {"timestamp": "2025-08-08T18:01:42Z", "value": 799},
                    "obdStatusDTCCount": {
                        "timestamp": "2025-08-08T18:48:44Z",
                        "value": 1,
                    },
                    "powertrainCombustionEngineECT": {
                        "timestamp": "2025-08-08T18:48:44Z",
                        "value": 30,
                    },
                    "powertrainCombustionEngineMAF": {
                        "timestamp": "2024-12-02T07:20:11Z",
                        "value": 0.05,
                    },
                    "powertrainCombustionEngineSpeed": {
                        "timestamp": "2025-08-08T18:45:53Z",
                        "value": 16383,
                    },
                    "powertrainCombustionEngineTPS": {
                        "timestamp": "2025-08-08T18:48:44Z",
                        "value": 0,
                    },
                    "powertrainFuelSystemAbsoluteLevel": {
                        "timestamp": "2025-02-27T14:24:36Z",
                        "value": 0,
                    },
                    "powertrainFuelSystemRelativeLevel": {
                        "timestamp": "2025-08-08T18:01:57Z",
                        "value": 81.17647058823529,
                    },
                    "powertrainRange": {
                        "timestamp": "2024-07-19T16:45:16.517921Z",
                        "value": 39,
                    },
                    "powertrainTractionBatteryChargingIsCharging": {
                        "timestamp": "2024-07-19T16:45:16.517921Z",
                        "value": 1,
                    },
                    "powertrainTractionBatteryRange": {
                        "timestamp": "2025-02-27T13:57:07Z",
                        "value": 0.125,
                    },
                    "powertrainTractionBatteryStateOfChargeCurrent": {
                        "timestamp": "2025-08-08T18:48:44Z",
                        "value": 95,
                    },
                    "powertrainTransmissionTravelledDistance": {
                        "timestamp": "2025-08-08T18:48:44Z",
                        "value": 11800,
                    },
                    "powertrainType": {
                        "timestamp": "2025-08-08T18:48:44Z",
                        "value": "COMBUSTION",
                    },
                    "speed": {"timestamp": "2025-08-08T18:48:44Z", "value": 0},
                },
            },
        }
    }
    dimo_mock.telemetry.query.return_value = query_result

    result = dimo_client.get_latest_signals_batched(token_id, signal_names)

    # Assert the result matches the query result
    assert result == query_result

    # Make sure the full query was batched into two queries
    assert dimo_mock.telemetry.query.call_count == 2
    auth_mock.get_privileged_token.assert_called_once_with(token_id)


def test_dimo_client_get_latest_signals_batched_empty():
    auth_mock = Mock()
    dimo_mock = Mock()
    priv_token = create_mock_token(3600)
    auth_mock.get_privileged_token.return_value = priv_token

    dimo_client = DimoClient(auth=auth_mock)
    dimo_client.dimo = dimo_mock  # Inject the dimo mock

    token_id = "777"
    signal_names = []  # Empty signal names

    # Call the method under test
    result = dimo_client.get_latest_signals_batched(token_id, signal_names)

    # Assert the result is an empty dictionary within 'data.signalsLatest'
    assert result == {"data": {"signalsLatest": {}}}


def test_dimo_client_get_latest_signals_batched_normal():
    auth_mock = Mock()
    dimo_mock = Mock()
    priv_token = create_mock_token(3600)
    auth_mock.get_privileged_token.return_value = priv_token

    dimo_client = DimoClient(auth=auth_mock)
    dimo_client.dimo = dimo_mock  # Inject the dimo mock

    token_id = "90019"
    signal_names = ["signal1", "signal2", "signal3"]
    query_result = {
        "data": {
            "signalsLatest": {
                "signal1": {"timestamp": "2025-08-08T12:00:00Z", "value": 10},
                "signal2": {"timestamp": "2025-08-08T12:01:00Z", "value": 20},
                "signal3": {"timestamp": "2025-08-08T12:02:00Z", "value": 30},
            }
        }
    }
    dimo_mock.telemetry.query.return_value = query_result

    # Call the method
    result = dimo_client.get_latest_signals_batched(token_id, signal_names)

    # Assert that the returned result matches the query result
    assert result == query_result
    dimo_mock.telemetry.query.assert_called_once()


def test_dimo_client_get_latest_signals_batched_complexity_error():
    auth_mock = Mock()
    dimo_mock = Mock()
    priv_token = create_mock_token(3600)
    auth_mock.get_privileged_token.return_value = priv_token

    dimo_client = DimoClient(auth=auth_mock)
    dimo_client.dimo = dimo_mock  # Inject the dimo mock

    token_id = "88001"
    signal_names = [f"signal{i}" for i in range(50)]  # Large number of signals to test chunking

    def complexity_error_simulation(query, vehicle_jwt):
        if len(query) > 250:
            raise RuntimeError("GraphQL complexity limit exceeded at minimum chunk size")
        return {"data": {"signalsLatest": {}}}

    dimo_mock.telemetry.query.side_effect = complexity_error_simulation
    # Capture the RuntimeError
    try:
        dimo_client.get_latest_signals_batched(token_id, signal_names)
    except RuntimeError as e:
        assert str(e) == "GraphQL complexity limit exceeded at minimum chunk size"


    # Arrange: Set up mocks
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    dimo_client = DimoClient(auth=auth_mock)
    token_id = "18003"

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
    token_id = "65999"

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

def test_dimo_client_lock_doors():
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    priv_token = create_mock_token(600)
    auth_mock.get_privileged_token.return_value = priv_token
    dimo_client = DimoClient(auth=auth_mock)
    token_id = "99994"
    dimo_mock.devices.lock_doors.return_value = {"result": "locked"}
    result = dimo_client.lock_doors(token_id)
    assert result == {"result": "locked"}
    dimo_mock.devices.lock_doors.assert_called_once_with(priv_token.token, token_id)
    auth_mock.get_privileged_token.assert_called_once_with(token_id)

def test_dimo_client_unlock_doors():
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    priv_token = create_mock_token(600)
    auth_mock.get_privileged_token.return_value = priv_token
    dimo_client = DimoClient(auth=auth_mock)
    token_id = "99995"
    dimo_mock.devices.unlock_doors.return_value = {"result": "unlocked"}
    result = dimo_client.unlock_doors(token_id)
    assert result == {"result": "unlocked"}
    dimo_mock.devices.unlock_doors.assert_called_once_with(priv_token.token, token_id)
    auth_mock.get_privileged_token.assert_called_once_with(token_id)

def test_fetch_privileged_token_success():
    auth_mock = Mock()
    priv_token = create_mock_token(1200)
    auth_mock.get_privileged_token.return_value = priv_token
    dimo_client = DimoClient(auth=auth_mock)
    token_id = "10234"
    # Patch auth.get_access_token to do nothing
    auth_mock.get_access_token.return_value = None
    result = dimo_client._fetch_privileged_token(token_id)
    assert result == priv_token.token
    auth_mock.get_access_token.assert_called_once()
    auth_mock.get_privileged_token.assert_called_once_with(token_id)

def test_fetch_privileged_token_exception():
    auth_mock = Mock()
    auth_mock.get_privileged_token.side_effect = Exception("fail")
    dimo_client = DimoClient(auth=auth_mock)
    token_id = "20345"
    auth_mock.get_access_token.return_value = None
    try:
        dimo_client._fetch_privileged_token(token_id)
        assert False, "Exception was not raised!"
    except Exception as e:
        assert str(e) == "fail"
    auth_mock.get_access_token.assert_called_once()
    auth_mock.get_privileged_token.assert_called_once_with(token_id)

def test_get_all_vehicles_for_license_default():
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    dimo_client = DimoClient(auth=auth_mock)
    auth_mock.client_id = "0xd9E311344F1eFA490C82615d3989687A5628afb4"
    dimo_mock.identity.query.return_value = {"vehicles": [1, 2, 3]}
    result = dimo_client.get_all_vehicles_for_license()
    assert result == {"vehicles": [1, 2, 3]}
    dimo_mock.identity.query.assert_called_once()
    assert 'privileged: "0xd9E311344F1eFA490C82615d3989687A5628afb4"' in dimo_mock.identity.query.call_args[0][0]

def test_get_all_vehicles_for_license_with_arg():
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    dimo_client = DimoClient(auth=auth_mock)
    dimo_mock.identity.query.return_value = {"vehicles": [42]}
    license_addr = "0xAbCdEf789012345678901234567890abcdef1234"
    result = dimo_client.get_all_vehicles_for_license(license_addr)
    assert result == {"vehicles": [42]}
    dimo_mock.identity.query.assert_called_once()
    assert f'privileged: "{license_addr}"' in dimo_mock.identity.query.call_args[0][0]

def test_merge_graphql_data_merges_responses():
    responses = [
        {"data": {"signalsLatest": {"a": 1, "b": 2}}, "errors": [1]},
        {"data": {"signalsLatest": {"b": 22, "c": 3}}},
        {"data": {"signalsLatest": {"z": 100}}, "errors": [2, 3]},
    ]
    merged = DimoClient._merge_graphql_data(responses)
    assert merged["data"]["signalsLatest"] == {"a": 1, "b": 22, "c": 3, "z": 100}
    assert merged["errors"] == [1, 2, 3]

def test_is_complexity_error_true():
    resp = {"errors": [
        {"message": "q is too complex", "extensions": {"code": "COMPLEXITY_LIMIT_EXCEEDED"}}
    ]}
    assert DimoClient._is_complexity_error(resp) is True

def test_is_complexity_error_false():
    assert not DimoClient._is_complexity_error({"errors": None})
    assert not DimoClient._is_complexity_error({"errors": [{"extensions": {"code": "OTHER_CODE"}}]})
    assert not DimoClient._is_complexity_error({})

def test_dimo_client_get_vin_keyerror():
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    dimo_client = DimoClient(auth=auth_mock)
    token_id = "82111"
    priv_token = create_mock_token(10)
    auth_mock.get_privileged_token.return_value = priv_token
    dimo_mock.telemetry.get_vin.side_effect = KeyError("failkey")
    vin = dimo_client.get_vin(token_id)
    assert vin is None
    auth_mock.get_privileged_token.assert_called_once_with(token_id)
    dimo_mock.telemetry.get_vin.assert_called_once_with(priv_token.token, token_id)

def test_dimo_client_get_vin_connection_error():
    import requests
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    dimo_client = DimoClient(auth=auth_mock)
    token_id = "73103"
    priv_token = create_mock_token(23)
    auth_mock.get_privileged_token.return_value = priv_token
    dimo_mock.telemetry.get_vin.side_effect = requests.exceptions.ConnectionError("test")
    vin = dimo_client.get_vin(token_id)
    assert vin is None
    auth_mock.get_privileged_token.assert_called_once_with(token_id)
    dimo_mock.telemetry.get_vin.assert_called_once_with(priv_token.token, token_id)

def test_dimo_client_get_vin_general_exception():
    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    dimo_client = DimoClient(auth=auth_mock)
    token_id = "82102"
    priv_token = create_mock_token(23)
    auth_mock.get_privileged_token.return_value = priv_token
    dimo_mock.telemetry.get_vin.side_effect = Exception("ohno")
    vin = dimo_client.get_vin(token_id)
    assert vin is None
    auth_mock.get_privileged_token.assert_called_once_with(token_id)
    dimo_mock.telemetry.get_vin.assert_called_once_with(priv_token.token, token_id)

def test_get_latest_signals_batched_unknown_exception():
    auth_mock = Mock()
    dimo_mock = Mock()
    priv_token = create_mock_token(20)
    auth_mock.get_privileged_token.return_value = priv_token
    dimo_client = DimoClient(auth=auth_mock)
    dimo_client.dimo = dimo_mock
    token_id = "56777"
    signal_names = ["sig1", "sig2"]
    # Simulate unknown exception in telemetry.query
    def raise_exc(*a, **kw):
        raise Exception("telemetry fail")
    dimo_mock.telemetry.query.side_effect = raise_exc
    try:
        dimo_client.get_latest_signals_batched(token_id, signal_names)
        assert False, "Exception should be reraised!"
    except Exception as ex:
        assert str(ex) == "telemetry fail"

    assert not DimoClient._is_complexity_error({"errors": None})
    assert not DimoClient._is_complexity_error({"errors": [{"extensions": {"code": "OTHER_CODE"}}]})
    assert not DimoClient._is_complexity_error({})

    auth_mock = Mock()
    auth_mock.get_privileged_token.side_effect = Exception("fail")
    dimo_client = DimoClient(auth=auth_mock)
    token_id = "55555"
    auth_mock.get_access_token.return_value = None
    try:
        dimo_client._fetch_privileged_token(token_id)
        assert False, "Exception was not raised!"
    except Exception as e:
        assert str(e) == "fail"
    auth_mock.get_access_token.assert_called_once()
    auth_mock.get_privileged_token.assert_called_once_with(token_id)

    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    priv_token = create_mock_token(600)
    auth_mock.get_privileged_token.return_value = priv_token
    dimo_client = DimoClient(auth=auth_mock)
    token_id = "58585"
    dimo_mock.devices.unlock_doors.return_value = {"result": "unlocked"}
    result = dimo_client.unlock_doors(token_id)
    assert result == {"result": "unlocked"}
    dimo_mock.devices.unlock_doors.assert_called_once_with(priv_token.token, token_id)
    auth_mock.get_privileged_token.assert_called_once_with(token_id)

    auth_mock = Mock()
    dimo_mock = auth_mock.get_dimo.return_value
    dimo_client = DimoClient(auth=auth_mock)

    dimo_mock.identity.count_dimo_vehicles.side_effect = Exception("API error")

    total_vehicles = dimo_client.get_total_dimo_vehicles()

    assert total_vehicles is None
    dimo_mock.identity.count_dimo_vehicles.assert_called_once()
