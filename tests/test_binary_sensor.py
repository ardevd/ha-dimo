from types import SimpleNamespace

import pytest

from custom_components.dimo.binary_sensor import DimoVehicleBinarySensorEntity


class DummyCoordinator:
    """A minimal stub for DimoUpdateCoordinator holding vehicle_data."""

    def __init__(self, vehicle_data, domain: str = "dimo"):
        self.vehicle_data = vehicle_data
        self.entry = SimpleNamespace(domain=domain)


def make_entity(coordinator, token, key):
    """Helper to construct the sensor entity."""
    return DimoVehicleBinarySensorEntity(coordinator, token, key)


def test_is_on_true():
    """When signal_data contains a truthy value, is_on returns True."""
    token = "123456"
    key = "currentLocationIsRedacted"

    vehicle = SimpleNamespace(signal_data={key: {"value": True}})
    coord = DummyCoordinator({token: vehicle})

    entity = make_entity(coord, token, key)
    assert entity.is_on is True


def test_is_on_false():
    """When signal_data contains a falsy value (False), is_on returns False."""
    token = "123456"
    key = "currentLocationIsRedacted"
    vehicle = SimpleNamespace(signal_data={key: {"value": False}})
    coord = DummyCoordinator({token: vehicle})

    entity = make_entity(coord, token, key)
    assert entity.is_on is False


def test_is_on_missing_signal_key():
    """When signal_data lacks the key, is_on returns None (unavailable)."""
    token = "1234566"
    key = "currentLocationIsRedacted"
    vehicle = SimpleNamespace(signal_data={})
    coord = DummyCoordinator({token: vehicle})

    entity = make_entity(coord, token, key)
    assert entity.is_on is None


def test_is_on_signal_none():
    """When signal_data[key] is None, is_on returns None without exception."""
    token = "12345676"
    key = "currentLocationIsRedacted"
    vehicle = SimpleNamespace(signal_data={key: None})
    coord = DummyCoordinator({token: vehicle})

    entity = make_entity(coord, token, key)
    assert entity.is_on is None


def test_is_on_missing_vehicle():
    """When the vehicle_token_id is not present, is_on returns None."""
    token = "123450900"
    key = "currentLocationIsRedacted"
    # coordinator has data for a different token
    other_vehicle = SimpleNamespace(signal_data={key: {"value": True}})
    coord = DummyCoordinator({"111222": other_vehicle})

    entity = make_entity(coord, token, key)
    assert entity.is_on is None
