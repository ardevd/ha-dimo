"""The DIMO integration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_CLIENT_ID
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CONF_AUTH_PROVIDER, CONF_PRIVATE_KEY, DOMAIN, PLATFORMS
from .dimoapi import Auth, DimoClient
from .helpers import get_key

_LOGGER = logging.getLogger(__name__)


@dataclass
class DIMOConfigData:
    """Class to hold integration data."""

    coordinator: DimoUpdateCoordinator


type DIMOConfigEntry = ConfigEntry[DIMOConfigData]


async def async_setup_entry(hass: HomeAssistant, entry: DIMOConfigEntry) -> bool:
    """Set up DIMO from a config entry."""

    auth = Auth(
        entry.data[CONF_CLIENT_ID],
        entry.data[CONF_AUTH_PROVIDER],
        entry.data[CONF_PRIVATE_KEY],
    )
    client = DimoClient(auth)
    try:
        await hass.async_add_executor_job(client.init)
    except Exception as ex:
        # TODO: Handle specific exceptions from api for failed token retrieval
        raise ConfigEntryNotReady from ex

    coordinator = DimoUpdateCoordinator(hass, entry, client)
    entry.runtime_data = DIMOConfigData(coordinator)
    await coordinator.async_initialise()
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_remove_config_entry_device(
    hass: HomeAssistant, config_entry, device_entry
) -> bool:
    """Delete device."""
    return True


async def async_unload_entry(hass: HomeAssistant, entry: DIMOConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


@dataclass
class VehicleData:
    """Class to hold vehicle data."""

    definition: dict
    available_signals: dict | None = None
    signal_data: dict | None = None
    signal_data_errors: dict | None = None


class DimoUpdateCoordinator(DataUpdateCoordinator):
    """Update coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: DIMOConfigEntry,
        client: DimoClient,
    ) -> None:
        """Initialise update coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} ({entry.unique_id})",
            update_method=self.async_update_data,
            update_interval=timedelta(seconds=30),
        )

        self.client = client
        self.entry = entry

        self.user_data: dict[str, Any] = {}
        self.vehicle_data: dict[str, VehicleData] = {}

    async def async_initialise(self):
        """Get initial static data."""
        await self.get_user_data()
        await self.get_vehicles_data()

        if self.vehicle_data:
            for vehicle_token_id in self.vehicle_data:
                await self.get_available_signals_for_vehicle(vehicle_token_id)

                self.create_vehicle_device(vehicle_token_id)

    async def get_user_data(self):
        """Get and store user data."""
        # TODO: Not sure if we need this - remove if not
        self.user_data = await self.hass.async_add_executor_job(
            self.client.dimo.user.user, self.client.auth.token
        )

    async def get_vehicles_data(self):
        """Get all vehicle data."""
        vehicles_data = await self.hass.async_add_executor_job(
            self.client.get_all_vehicles_for_license, self.entry.data[CONF_CLIENT_ID]
        )
        vehicles = get_key("data.vehicles.nodes", vehicles_data)
        for vehicle in vehicles:
            vehicle_token_id = vehicle.get("tokenId")

            self.vehicle_data[vehicle_token_id] = VehicleData(
                definition=vehicle.get("definition")
            )

    async def get_available_signals_for_vehicle(self, vehicle_token_id: str):
        """Get available signals for vehicle by token_id."""

        # Validate vehicle is in our list
        if vehicle_token_id in self.vehicle_data:
            available_signals_data = await self.hass.async_add_executor_job(
                self.client.get_available_signals, vehicle_token_id
            )
            if available_signals_data:
                self.vehicle_data[vehicle_token_id].available_signals = get_key(
                    "data.availableSignals", available_signals_data
                )
            _LOGGER.debug(
                "AVAILABLE SIGNALS: %s - %s", vehicle_token_id, available_signals_data
            )
        else:
            _LOGGER.error(
                "Unable to fetch available signals data for %s.  Not a known vehicle on this account",
                vehicle_token_id,
            )

    async def get_signals_data_for_vehicle(self, vehicle_token_id: str):
        """Get data for list of available signals for vehicle."""
        if self.vehicle_data.get(vehicle_token_id):
            signals_data = await self.hass.async_add_executor_job(
                self.client.get_latest_signals,
                vehicle_token_id,
                self.vehicle_data[vehicle_token_id].available_signals,
            )
            _LOGGER.debug("SIGNALS DATA: %s", signals_data)
            self.vehicle_data[vehicle_token_id].signal_data = get_key(
                "data.signalsLatest", signals_data
            )
            self.vehicle_data[vehicle_token_id].signal_data_errors = get_key(
                "errors", signals_data
            )
        else:
            _LOGGER.error(
                "Unable to fetch signals data for %s.  Not a known vehicle on this account",
                vehicle_token_id,
            )

    async def async_update_data(self):
        """Update data from api."""
        _LOGGER.debug("Updating from api")
        for vehicle_token_id in self.vehicle_data:
            await self.get_signals_data_for_vehicle(vehicle_token_id)

        return True

    def create_vehicle_device(self, vehicle_token_id: str):
        """Create device for vehicle."""
        vehicle = self.vehicle_data[vehicle_token_id]
        device_registry = dr.async_get(self.hass)
        device_registry.async_get_or_create(
            config_entry_id=self.entry.entry_id,
            identifiers={(DOMAIN, vehicle_token_id)},
            manufacturer=vehicle.definition["make"],
            name=f"{vehicle.definition["make"]} {vehicle.definition["model"]}",
            model=vehicle.definition["model"],
        )
