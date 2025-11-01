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


class _DimoSensorMixin:
    """Mixin that implements the SensorEntity interface in terms of two helper methods"""

    @property
    def native_value(self):
        return self._get_value()

    @property
    def native_unit_of_measurement(self) -> str | None:
        return self._get_unit()

    def _get_value(self):
        raise NotImplementedError

    def _get_unit(self):
        raise NotImplementedError


class DimoSensorEntity(DimoBaseEntity, _DimoSensorMixin, SensorEntity):
    """Non‐vehicle sensors come from coordinator.dimo_data."""

    def _get_value(self):
        return self.coordinator.dimo_data.get(self.key)

    def _get_unit(self):
        return (
            DIMO_SENSORS[self.key].unit_of_measure
            if DIMO_SENSORS.get(self.key)
            else None
        )


class DimoVehicleSensorEntity(DimoBaseVehicleEntity, _DimoSensorMixin, SensorEntity):
    """Vehicle sensors come from the per‑vehicle signal_data blob."""

    def _get_value(self):
        vehicle = self.coordinator.vehicle_data.get(self.vehicle_token_id, {})
        data = getattr(vehicle, "signal_data", {}).get(self.key)
        return data.get("value") if data else None

    def _get_unit(self):
        return SIGNALS[self.key].unit_of_measure if SIGNALS.get(self.key) else None
