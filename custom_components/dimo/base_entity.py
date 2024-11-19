"""Handles sensor entities."""

import logging
from typing import Any

from config.custom_components.dimo.const import SIGNALS
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DimoUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class DimoBaseEntity(CoordinatorEntity):
    """Base entity."""

    _attr_has_entity_name = True

    def __init__(
        self, coordinator: DimoUpdateCoordinator, vehicle_token_id: str, key: str
    ) -> None:
        """Initialise."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.vehicle_token_id = vehicle_token_id
        self.key = key

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("%s device update requested", self.name)

    @property
    def name(self):
        """Return the name of the sensor."""
        return SIGNALS[self.key].name if SIGNALS.get(self.key) else self.key

    @property
    def icon(self) -> str | None:
        """Return the icon to use in the frontend, if any."""
        return SIGNALS[self.key].icon if SIGNALS.get(self.key) else None

    @property
    def device_class(self) -> BinarySensorDeviceClass | SensorDeviceClass | None:
        """Return the class of this entity."""
        return SIGNALS[self.key].device_class if SIGNALS.get(self.key) else None

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
