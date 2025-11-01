import logging
from unittest.mock import MagicMock, patch

import dimo as dimo_sdk
import pytest
from homeassistant.core import HomeAssistant

from custom_components.dimo import DOMAIN
from custom_components.dimo.__init__ import DimoUpdateCoordinator, VehicleData


@pytest.fixture
def hass() -> HomeAssistant:
    """Return a dummy HomeAssistant instance."""
    return MagicMock(spec=HomeAssistant)


@pytest.fixture
def entry():
    """Return a dummy config entry."""
    entry = MagicMock()
    entry.entry_id = "test_entry"
    # Populate the required data for the integration.
    entry.data = {
        "client_id": "dummy_client_id",
        "auth_provider": "dummy_provider",
        "private_key": "dummy_key",
    }
    return entry


@pytest.fixture
def client():
    """Return a dummy DimoClient with a stubbed get_vin method."""
    client = MagicMock()
    client.get_vin = MagicMock(return_value="ABAH294120SJ1A21")
    return client


@pytest.fixture
def coordinator(hass, entry, client):
    """Return an instance of DimoUpdateCoordinator with a dummy vehicle in vehicle_data."""
    coordinator = DimoUpdateCoordinator(hass, entry, client)
    # Add dummy vehicle data with a known token ID.
    vehicle_token_id = "41221"
    coordinator.vehicle_data[vehicle_token_id] = VehicleData(
        definition={"make": "TestMake", "model": "TestModel"}
    )
    return coordinator


@pytest.mark.asyncio
async def test_get_vehicle_vin_success(coordinator):
    """Test that _get_vehicle_vin sets the VIN when get_api_data returns a VIN."""
    vehicle_token_id = "41221"
    expected_vin = "ABAH294120SJ1A21"
    # Patch get_api_data to return a valid VIN.
    with patch.object(
        coordinator, "get_api_data", return_value=expected_vin
    ) as mock_get_api_data:
        await coordinator._get_vehicle_vin(vehicle_token_id)
        # Verify that get_api_data was called with the client's get_vin and vehicle_token_id.
        mock_get_api_data.assert_called_once_with(
            coordinator.client.get_vin, vehicle_token_id
        )
        # Check that the VIN is stored on the vehicle data.
        assert coordinator.vehicle_data[vehicle_token_id].vin == expected_vin


def test_create_vehicle_device_with_vin(coordinator):
    """Test create_vehicle_device for a vehicle with a VIN."""

    vehicle_token_id = "41221"
    vin_value = "ABAH294120SJ1A21"
    # Set the VIN on the vehicle data.
    vehicle = coordinator.vehicle_data[vehicle_token_id]
    vehicle.vin = vin_value

    # Create a dummy device registry object.
    device_registry = MagicMock()

    # Patch the device registry lookup used in create_vehicle_device.
    with patch(
        "custom_components.dimo.__init__.dr.async_get", return_value=device_registry
    ) as mock_async_get:
        coordinator.create_vehicle_device(vehicle_token_id)

    # The expected identifiers should include both the token and the VIN.
    expected_identifiers = {(DOMAIN, vehicle_token_id), (DOMAIN, vin_value)}
    device_registry.async_get_or_create.assert_called_once_with(
        config_entry_id=coordinator.entry.entry_id,
        identifiers=expected_identifiers,
        manufacturer=vehicle.definition["make"],
        name=f'{vehicle.definition["make"]} {vehicle.definition["model"]}',
        model=vehicle.definition["model"],
    )


@pytest.mark.asyncio
async def test_get_api_data_http_error_returns_none(coordinator, caplog):
    """get_api_data should log a warning and return None on dimo_sdk.HTTPError."""
    caplog.set_level(logging.WARNING)
    dummy_fn = lambda: None
    http_err = dimo_sdk.request.HTTPError(status=502, message="timeout")
    with patch.object(coordinator.hass, "async_add_executor_job", side_effect=http_err):
        result = await coordinator.get_api_data(dummy_fn, "arg1", "arg2")
    assert result is None
    assert "dimo api request http error" in caplog.text.lower()
