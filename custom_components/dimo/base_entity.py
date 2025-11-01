"""Handles sensor entities."""

import logging
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.dimo.const import SignalDef

from . import DimoUpdateCoordinator
from .const import DIMO_SENSORS, DOMAIN, SIGNALS

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

        sensor_def = DIMO_SENSORS.get(key)
        if sensor_def:
            self._attr_name = sensor_def.name
            self._attr_icon = sensor_def.icon
            self._attr_device_class = sensor_def.device_class
            self._attr_state_class = sensor_def.state_class
        else:
            # Fallbacks if the key isn't found in DIMO_SENSORS
            self._attr_name = key
            self._attr_icon = None
            self._attr_device_class = None
            self._attr_state_class = None

        self._attr_unique_id = f"{coordinator.entry.domain}_{vehicle_token_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.entry.domain, vehicle_token_id)}
        )

        # Use the built-in feature to automatically adopt the device's name
        self._attr_has_entity_name = True

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("%s device update requested", self.name)
        try:
            self.async_write_ha_state()
        except KeyError as err:
            _LOGGER.warning("Failed to update %s: %s", self.name, err)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {}

    @property
    def available(self) -> bool:
        """Return whether data is available for this entity."""
        vehicle = self.coordinator.vehicle_data.get(self.vehicle_token_id)
        return bool(vehicle and vehicle.signal_data.get(self.key))


class DimoBaseVehicleEntity(DimoBaseEntity):
    """Base representation of a vehicle entity."""

    @property
    def _signal(self) -> SignalDef | None:
        """Return the signal config if present."""
        return SIGNALS.get(self.key)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        if self._signal and self._signal.name:
            return self._signal.name
        return self.key

    @property
    def icon(self) -> str | None:
        """Return the icon to use in the frontend, if any."""
        return self._signal.icon if self._signal else None

    @property
    def device_class(self) -> BinarySensorDeviceClass | SensorDeviceClass | None:
        """Return the class of this entity."""
        return self._signal.device_class if self._signal else None

    @property
    def state_class(self) -> SensorStateClass | str | None:
        """Return the state class of this entity, if any."""
        return self._signal.state_class if self._signal else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        vehicle_data = self.coordinator.vehicle_data[self.vehicle_token_id]
        signal_data = vehicle_data.signal_data.get(self.key, {})

        extra_attr = {"timestamp": signal_data.get("timestamp")}

        return extra_attr

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for the vehicle, including its VIN if available."""
        vehicle = self.coordinator.vehicle_data[self.vehicle_token_id]
        identifiers = {(DOMAIN, self.vehicle_token_id)}
        vin = ""
        parent = (DOMAIN, DOMAIN)
        if vehicle.vin:
            identifiers.add((DOMAIN, vehicle.vin))
            vin = vehicle.vin

        return DeviceInfo(
            identifiers=identifiers,
            manufacturer=vehicle.definition.get("make", "DIMO"),
            name=f"{vehicle.definition.get('make', 'Unknown')} {vehicle.definition.get('model', 'Unknown')}",
            model=vehicle.definition.get("model", "Unknown Model"),
            serial_number=vin,
            via_device=parent,
        )
