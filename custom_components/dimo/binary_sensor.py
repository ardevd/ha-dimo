"""Handles sensor entities."""

import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DIMOConfigEntry
from .base_entity import DimoBaseEntity, DimoBaseVehicleEntity
from .const import DIMO_SENSORS, DOMAIN, SIGNALS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DIMOConfigEntry,
    add_entities: AddEntitiesCallback,
):
    """Initialise binary sensor platform."""

    coordinator = entry.runtime_data.coordinator

    entities = []

    # Add Dimo entities
    entities.extend(
        [
            DimoBinarySensorEntity(coordinator, DOMAIN, key)
            for key, sensor_def in DIMO_SENSORS.items()
            if sensor_def.platform == Platform.BINARY_SENSOR
        ]
    )

    # Add vehicle entities
    for vehicle_token_id, vehicle_data in coordinator.vehicle_data.items():
        entities.extend(
            [
                DimoVehicleBinarySensorEntity(coordinator, vehicle_token_id, key)
                for key in vehicle_data.signal_data
                if vehicle_data.signal_data[key]
                and SIGNALS.get(key)
                and SIGNALS[key].platform == Platform.BINARY_SENSOR
            ]
        )

    add_entities(entities)


class DimoBinarySensorEntity(DimoBaseEntity, BinarySensorEntity):
    """Binary Sensor entity."""

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self.coordinator.dimo_data.get(self.key)


class DimoVehicleBinarySensorEntity(DimoBaseVehicleEntity, BinarySensorEntity):
    """Binary Sensor entity."""

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        vehicle = self.coordinator.vehicle_data.get(self.vehicle_token_id)
        if vehicle is None:
            return None

        signal = vehicle.signal_data.get(self.key)
        if not signal or "value" not in signal:
            return None

        return signal.get("value")
