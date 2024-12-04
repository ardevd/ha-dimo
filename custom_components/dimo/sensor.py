"""Handles sensor entities."""

import logging

from homeassistant.components.sensor import SensorEntity
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
    """Initialise sensor platform."""

    coordinator = entry.runtime_data.coordinator

    entities = []

    # Add Dimo entities
    entities.extend(
        [
            DimoSensorEntity(coordinator, DOMAIN, key)
            for key, sensor_def in DIMO_SENSORS.items()
            if sensor_def.platform == Platform.SENSOR
        ]
    )

    # Add vehicle entities
    for vehicle_token_id, vehicle_data in coordinator.vehicle_data.items():
        entities.extend(
            [
                DimoVehicleSensorEntity(coordinator, vehicle_token_id, key)
                for key in vehicle_data.signal_data
                if vehicle_data.signal_data[key]
                and (
                    (SIGNALS.get(key) and SIGNALS[key].platform == Platform.SENSOR)
                    or not SIGNALS.get(key)
                )
            ]
        )

    add_entities(entities)


class DimoSensorEntity(DimoBaseEntity, SensorEntity):
    """Dimo sensor entity."""

    @property
    def native_value(self):
        """Return the native value of this entity."""
        return self.coordinator.dimo_data.get(self.key)

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement of the sensor, if any."""
        return (
            DIMO_SENSORS[self.key].unit_of_measure
            if DIMO_SENSORS.get(self.key)
            else None
        )


class DimoVehicleSensorEntity(DimoBaseVehicleEntity, SensorEntity):
    """Vehicle Sensor entity."""

    @property
    def native_value(self):
        """Return the native value of this entity."""
        return (
            self.coordinator.vehicle_data[self.vehicle_token_id]
            .signal_data[self.key]
            .get("value")
        )

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement of the sensor, if any."""
        return SIGNALS[self.key].unit_of_measure if SIGNALS.get(self.key) else None
