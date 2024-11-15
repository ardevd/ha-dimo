"""Handles sensor entities."""

import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DIMOConfigEntry
from .base_entity import DimoBaseEntity
from .const import SIGNALS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DIMOConfigEntry,
    add_entities: AddEntitiesCallback,
):
    """Initialise binary sensor platform."""

    coordinator = entry.runtime_data.coordinator

    entities = []

    for vehicle_token_id, vehicle_data in coordinator.vehicle_data.items():
        entities.extend(
            [
                DimoSensorEntity(coordinator, vehicle_token_id, key)
                for key in vehicle_data.signal_data
                if vehicle_data.signal_data[key]
                and SIGNALS.get(key)
                and SIGNALS[key].platform == Platform.BINARY_SENSOR
            ]
        )

    add_entities(entities)


class DimoSensorEntity(DimoBaseEntity, BinarySensorEntity):
    """Binary Sensor entity."""

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return (
            self.coordinator.vehicle_data[self.vehicle_token_id]
            .signal_data[self.key]
            .get("value")
        )
