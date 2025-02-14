"""Handles device tracker entities."""

import logging

from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DIMOConfigEntry, DimoUpdateCoordinator
from .base_entity import DimoBaseVehicleEntity

_LOGGER = logging.getLogger(__name__)

LONG_KEY = "currentLocationLongitude"
LAT_KEY = "currentLocationLatitude"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DIMOConfigEntry,
    add_entities: AddEntitiesCallback,
):
    """Initialise sensor platform."""

    coordinator = entry.runtime_data.coordinator

    entities = []

    for vehicle_token_id, vehicle_data in coordinator.vehicle_data.items():
        latitude = vehicle_data.signal_data.get(LAT_KEY, {}).get("value")
        longitude = vehicle_data.signal_data.get(LONG_KEY, {}).get("value")

        if latitude is not None and longitude is not None:
            entities.append(
                DimoTrackerEntity(coordinator, vehicle_token_id, LAT_KEY, LONG_KEY)
            )

    add_entities(entities)

class DimoTrackerEntity(DimoBaseVehicleEntity, TrackerEntity):
    """Sensor entity."""

    def __init__(
        self,
        coordinator: DimoUpdateCoordinator,
        vehicle_token_id: str,
        latitude_key: str,
        longitude_key: str,
    ) -> None:
        """Initialise."""
        super().__init__(coordinator, vehicle_token_id, longitude_key)
        self._latitude_key = latitude_key
        self._longitude_key = longitude_key

    @property
    def source_type(self) -> str:
        """Return source type of the device"""
        return "gps"

    @property
    def extra_state_attributes(self):
        """Return additional tracker attributes"""
        data = self.coordinator.vehicle_data[self.vehicle_token_id].signal_data
        return {"altitude": data.get("currentLocationAltitude", {}).get("value")}

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        return (
            self.coordinator.vehicle_data[self.vehicle_token_id]
            .signal_data[self._latitude_key]
            .get("value")
        )

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        return (
            self.coordinator.vehicle_data[self.vehicle_token_id]
            .signal_data[self._longitude_key]
            .get("value")
        )
