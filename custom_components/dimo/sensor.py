"""Handles sensor entities."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DIMOConfigEntry, DimoUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DIMOConfigEntry,
    add_entities: AddEntitiesCallback,
):
    """Initialise sensor platform."""

    coordinator = entry.runtime_data.coordinator

    entities = []

    for vehicle_token_id, vehicle_data in coordinator.vehicle_data.items():
        entities.extend(
            [
                DimoSensorEntity(coordinator, vehicle_token_id, key)
                for key in vehicle_data.signal_data
                if vehicle_data.signal_data[key]
            ]
        )

    add_entities(entities)


class DimoSensorEntity(CoordinatorEntity, SensorEntity):
    """Sensor entity."""

    _attr_has_entity_name = True

    # TODO: Some sort of lookup for signals to name, device class and uom

    def __init__(
        self, coordinator: DimoUpdateCoordinator, vehicle_token_id: str, key: str
    ) -> None:
        """Initialise."""
        super().__init__(coordinator)

        self.vehicle_token_id = vehicle_token_id
        self.key = key

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("%s device update requested", self.name)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.key

    @property
    def native_value(self):
        """Return the native value of this entity."""
        return (
            self.coordinator.vehicle_data[self.vehicle_token_id]
            .signal_data[self.key]
            .get("value")
        )

    @property
    def unique_id(self):
        """Return uniqueid."""
        return f"{self.coordinator.entry.domain}_{self.vehicle_token_id}_{self.key}"

    @property
    def device_info(self):
        """Return device specific attributes."""
        return DeviceInfo(
            identifiers={(self.coordinator.entry.domain, self.vehicle_token_id)}
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {
            "timestamp": self.coordinator.vehicle_data[self.vehicle_token_id]
            .signal_data[self.key]
            .get("timestamp")
        }
