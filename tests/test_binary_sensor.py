from types import SimpleNamespace


from custom_components.dimo.binary_sensor import DimoVehicleBinarySensorEntity


def make_entity(coordinator, token, key):
    """Helper to construct the sensor entity."""
    return DimoVehicleBinarySensorEntity(coordinator, token, key)


def test_is_on_true(dummy_coordinator):
    """When signal_data contains a truthy value, is_on returns True."""
    token = "123456"
    key = "currentLocationIsRedacted"

    vehicle = SimpleNamespace(signal_data={key: {"value": True}})
    dummy_coordinator.vehicle_data = {token: vehicle}

    entity = make_entity(dummy_coordinator, token, key)
    assert entity.is_on is True


def test_is_on_false(dummy_coordinator):
    """When signal_data contains a falsy value (False), is_on returns False."""
    token = "123456"
    key = "currentLocationIsRedacted"
    vehicle = SimpleNamespace(signal_data={key: {"value": False}})
    dummy_coordinator.vehicle_data = {token: vehicle}

    entity = make_entity(dummy_coordinator, token, key)
    assert entity.is_on is False


def test_is_on_missing_signal_key(dummy_coordinator):
    """When signal_data lacks the key, is_on returns None (unavailable)."""
    token = "1234566"
    key = "currentLocationIsRedacted"
    vehicle = SimpleNamespace(signal_data={})
    dummy_coordinator.vehicle_data = {token: vehicle}

    entity = make_entity(dummy_coordinator, token, key)
    assert entity.is_on is None


def test_is_on_signal_none(dummy_coordinator):
    """When signal_data[key] is None, is_on returns None without exception."""
    token = "12345676"
    key = "currentLocationIsRedacted"
    vehicle = SimpleNamespace(signal_data={key: None})

    dummy_coordinator.vehicle_data = {token: vehicle}
    entity = make_entity(dummy_coordinator, token, key)
    assert entity.is_on is None


def test_is_on_missing_vehicle(dummy_coordinator):
    """When the vehicle_token_id is not present, is_on returns None."""
    token = "123450900"
    key = "currentLocationIsRedacted"
    # coordinator has data for a different token
    other_vehicle = SimpleNamespace(signal_data={key: {"value": True}})

    dummy_coordinator.vehicle_data = {"111222": other_vehicle}

    entity = make_entity(dummy_coordinator, token, key)
    assert entity.is_on is None
