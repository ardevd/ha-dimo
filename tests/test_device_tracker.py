from types import SimpleNamespace


from custom_components.dimo.device_tracker import DimoTrackerEntity
from custom_components.dimo.device_tracker import LAT_KEY
from custom_components.dimo.device_tracker import LONG_KEY


class DummyCoordinator:
    """A minimal stub for DimoUpdateCoordinator holding vehicle_data."""

    # TODO: Dont duplicate this
    def __init__(self, vehicle_data, domain: str = "dimo"):
        self.vehicle_data = vehicle_data
        self.entry = SimpleNamespace(domain=domain)


def make_entity(coordinator, token):
    """Helper to construct the sensor entity."""
    return DimoTrackerEntity(coordinator, token, LAT_KEY, LONG_KEY)


def test_latitude_longitude_properties():
    """Test that latitude and longitude properties return expected values."""

    token = "123456"
    vehicle = SimpleNamespace(
        signal_data={LAT_KEY: {"value": 59.9127}, LONG_KEY: {"value": 10.7461}}
    )
    coord = DummyCoordinator({token: vehicle})
    entity = make_entity(coord, token)

    assert entity.latitude == 59.9127
    assert entity.longitude == 10.7461
