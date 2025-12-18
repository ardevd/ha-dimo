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
    entry.options = {}
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


@pytest.mark.asyncio
async def test_async_update_options_reloads_entry():
    """Test that async_update_options triggers a config entry reload."""
    from custom_components.dimo import async_update_options

    # Create a mock HomeAssistant instance
    hass = MagicMock(spec=HomeAssistant)
    
    # Create a mock config entry
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    
    # Mock the async_reload method to return a coroutine
    async def mock_async_reload(entry_id):
        return True
    
    hass.config_entries.async_reload = MagicMock(side_effect=mock_async_reload)
    
    # Call async_update_options
    await async_update_options(hass, entry)
    
    # Verify that async_reload was called with the correct entry_id
    hass.config_entries.async_reload.assert_called_once_with("test_entry_id")


@pytest.mark.asyncio
async def test_update_listener_registered_on_setup():
    """Test that update listener is registered during async_setup_entry."""
    from custom_components.dimo import async_setup_entry, DOMAIN
    from custom_components.dimo.const import CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL
    
    # Create a mock HomeAssistant instance
    hass = MagicMock(spec=HomeAssistant)
    hass.config_entries = MagicMock()
    
    # Mock async_forward_entry_setups to return a coroutine
    async def mock_forward_setups(entry, platforms):
        return True
    
    hass.config_entries.async_forward_entry_setups = MagicMock(side_effect=mock_forward_setups)
    
    # Create a mock config entry
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.unique_id = "test_unique_id"
    entry.data = {
        "client_id": "test_client_id",
        "auth_provider": "test_provider",
        "private_key": "test_key",
    }
    entry.options = {CONF_POLL_INTERVAL: 60}
    
    # Track the update listener
    update_listener = None
    
    def mock_add_update_listener(listener):
        nonlocal update_listener
        update_listener = listener
        return MagicMock()  # Return a mock unload function
    
    entry.add_update_listener = mock_add_update_listener
    entry.async_on_unload = MagicMock()
    
    # Mock the DimoClient initialization
    with patch("custom_components.dimo.DimoClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.init = MagicMock()
        
        # Mock async_add_executor_job to simulate successful client init
        async def mock_executor_job(func, *args):
            return None
        
        hass.async_add_executor_job = mock_executor_job
        
        # Mock the coordinator to avoid full initialization
        with patch("custom_components.dimo.DimoUpdateCoordinator") as mock_coordinator_class:
            mock_coordinator = MagicMock()
            mock_coordinator_class.return_value = mock_coordinator
            
            # Make async methods return coroutines
            async def mock_async_initialise():
                return None
            
            async def mock_async_refresh():
                return None
            
            mock_coordinator.async_initialise = MagicMock(side_effect=mock_async_initialise)
            mock_coordinator.async_config_entry_first_refresh = MagicMock(side_effect=mock_async_refresh)
            
            # Call async_setup_entry
            result = await async_setup_entry(hass, entry)
            
            # Verify setup succeeded
            assert result is True
            
            # Verify that add_update_listener was called
            assert update_listener is not None
            
            # Verify async_on_unload was called
            entry.async_on_unload.assert_called_once()


@pytest.mark.asyncio
async def test_poll_interval_from_options():
    """Test that poll interval is correctly read from options."""
    from custom_components.dimo import DimoUpdateCoordinator
    from custom_components.dimo.const import CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL
    
    # Create a mock HomeAssistant instance
    hass = MagicMock(spec=HomeAssistant)
    
    # Create a mock config entry with custom poll interval
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.unique_id = "test_unique_id"
    entry.data = {
        "client_id": "test_client_id",
        "auth_provider": "test_provider",
        "private_key": "test_key",
    }
    entry.options = {CONF_POLL_INTERVAL: 120}
    
    # Create a mock client
    client = MagicMock()
    
    # Create the coordinator
    coordinator = DimoUpdateCoordinator(hass, entry, client)
    
    # Verify that the update_interval is set correctly
    assert coordinator.update_interval.total_seconds() == 120


@pytest.mark.asyncio
async def test_poll_interval_default_when_not_in_options():
    """Test that default poll interval is used when not specified in options."""
    from custom_components.dimo import DimoUpdateCoordinator
    from custom_components.dimo.const import CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL
    
    # Create a mock HomeAssistant instance
    hass = MagicMock(spec=HomeAssistant)
    
    # Create a mock config entry without poll interval in options
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.unique_id = "test_unique_id"
    entry.data = {
        "client_id": "test_client_id",
        "auth_provider": "test_provider",
        "private_key": "test_key",
    }
    entry.options = {}
    
    # Create a mock client
    client = MagicMock()
    
    # Create the coordinator
    coordinator = DimoUpdateCoordinator(hass, entry, client)
    
    # Verify that the update_interval is set to the default
    assert coordinator.update_interval.total_seconds() == DEFAULT_POLL_INTERVAL
