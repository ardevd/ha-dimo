import pytest

from types import SimpleNamespace


class DummyCoordinator:
    """A minimal stub for DimoUpdateCoordinator holding vehicle_data."""

    def __init__(self, vehicle_data, domain: str = "dimo"):
        self.vehicle_data = vehicle_data
        self.entry = SimpleNamespace(domain=domain)


@pytest.fixture
def dummy_coordinator():
    """Fixture providing a reusable DummyCoordinator."""
    return DummyCoordinator(vehicle_data={})
