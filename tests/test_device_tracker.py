from types import SimpleNamespace
from custom_components.dimo.device_tracker import DimoTrackerEntity, LAT_KEY, LONG_KEY


def test_latitude_longitude_properties(dummy_coordinator):
    """It should read latitude and longitude from the coordinator data."""
    token = "123456"
    vehicle = SimpleNamespace(
        signal_data={
            LAT_KEY: {"value": 59.9127},
            LONG_KEY: {"value": 10.7461},
        }
    )

    dummy_coordinator.vehicle_data = {token: vehicle}
    entity = DimoTrackerEntity(dummy_coordinator, token, LAT_KEY, LONG_KEY)

    assert entity.latitude == 59.9127
    assert entity.longitude == 10.7461
