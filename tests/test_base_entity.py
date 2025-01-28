import pytest
from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.dimo.base_entity import DimoBaseEntity
from custom_components.dimo.const import DIMO_SENSORS


@pytest.fixture
def mock_coordinator() -> DataUpdateCoordinator:
    """Return a mock coordinator for testing."""
    coordinator = MagicMock(spec=DataUpdateCoordinator)
    coordinator.entry = MagicMock()
    coordinator.entry.domain = "dimo"
    return coordinator


@pytest.mark.parametrize(
    "sensor_key, sensor_def",
    [
        (
            "mock_key_with_def",
            MagicMock(
                name="Total Dimo Vehicles",
                icon="mdi:counter",
                device_class="battery",
                state_class="total",
            ),
        ),
        (
            "mock_key_no_def",
            None,  # This tests the fallback path
        ),
    ],
)
def test_dimo_base_entity_init_sets_attributes(
    hass: HomeAssistant,
    mock_coordinator: DataUpdateCoordinator,
    sensor_key: str,
    sensor_def: MagicMock | None,
):
    """Test that DimoBaseEntity sets up attributes correctly on init."""
    vehicle_token_id = "1234"

    # Patch DIMO_SENSORS to return our mock sensor definitions for testing
    with patch.dict(DIMO_SENSORS, {}, clear=True):
        if sensor_def:
            # Insert our mock definition into DIMO_SENSORS
            DIMO_SENSORS[sensor_key] = sensor_def

        # Create the entity
        entity = DimoBaseEntity(mock_coordinator, vehicle_token_id, sensor_key)

        # Common attributes
        assert entity.vehicle_token_id == vehicle_token_id
        assert entity.key == sensor_key
        assert entity.coordinator == mock_coordinator

        # If we had a definition
        if sensor_def:
            assert entity.name == sensor_def.name
            assert entity.icon == sensor_def.icon
        else:
            # Fallbacks
            assert entity.name == sensor_key
            assert entity.icon is None
            assert entity.device_class is None

        # Unique ID
        expected_unique_id = (
            f"{mock_coordinator.entry.domain}_{vehicle_token_id}_{sensor_key}"
        )
        assert entity.unique_id == expected_unique_id

        # DeviceInfo check
        assert isinstance(entity.device_info, dict)
        assert entity.device_info["identifiers"] == {("dimo", vehicle_token_id)}
        # Make sure the entity has entity name
        assert entity.has_entity_name is True


def test_dimo_base_entity_handle_coordinator_update(
    hass: HomeAssistant, mock_coordinator: DataUpdateCoordinator
):
    """Test that _handle_coordinator_update calls async_write_ha_state."""
    entity = DimoBaseEntity(mock_coordinator, "vehicle_123", "mock_key")
    entity.hass = hass

    with patch.object(entity, "async_write_ha_state") as mock_write_ha_state:
        entity._handle_coordinator_update()
        mock_write_ha_state.assert_called_once()


def test_dimo_base_entity_extra_state_attributes(
    hass: HomeAssistant, mock_coordinator: DataUpdateCoordinator
):
    """Test extra_state_attributes returns an empty dict by default."""
    entity = DimoBaseEntity(mock_coordinator, "123456", "mock_key")
    entity.hass = hass

    assert entity.extra_state_attributes == {}
