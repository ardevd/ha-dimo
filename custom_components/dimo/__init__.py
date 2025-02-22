"""The DIMO integration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta, datetime, timezone
import logging
import asyncio
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_CLIENT_ID
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .config_flow import InvalidAuth, NoVehiclesException
from .const import CONF_AUTH_PROVIDER, CONF_PRIVATE_KEY, DIMO_SENSORS, DOMAIN, PLATFORMS
from .dimoapi import (
    Auth,
    DimoClient,
    InvalidApiKeyFormat,
    InvalidClientIdError,
    InvalidCredentialsError,
)
from .helpers import get_key
from typing import Optional

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
    except (
        InvalidAuth,
        InvalidClientIdError,
        InvalidCredentialsError,
        InvalidApiKeyFormat,
    ):
        _LOGGER.error(
            "Unable to setup Dimo integration due to invalid credentials.  Please check them and try again"
        )
        return False
    except NoVehiclesException as ex:
        _LOGGER.error(
            "Unable to setup Dimo integration due to having no vehicles shared with your account.  Please check you have vehicles shared"
        )
        raise ConfigEntryNotReady from ex
    except Exception as ex:
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
    vin: Optional[str] = None
    available_signals: Optional[dict] = None
    signal_data: Optional[dict] = None
    signal_data_errors: Optional[dict] = None


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

        self.dimo_data: dict[str, Any] = {}
        self.vehicle_data: dict[str, VehicleData] = {}

    async def async_initialise(self):
        """Get initial static data."""
        await self.get_vehicles_data()

        # Add Dimo device for non vehicle specificic sensors
        if DIMO_SENSORS:
            self.create_dimo_device()
            await self.get_dimo_sensor_data()

        if self.vehicle_data:
            # Fetch available signals for all available vehicles concurrently
            await asyncio.gather(
                *[
                    self.get_available_signals_for_vehicle(vehicle_token_id)
                    for vehicle_token_id in self.vehicle_data
                ]
            )
            # Create devices for each vehicle
            for vehicle_token_id in self.vehicle_data:
                # Grab VIN before creating
                await self._get_vehicle_vin(vehicle_token_id)
                self.create_vehicle_device(vehicle_token_id)

    async def get_dimo_sensor_data(self):
        """Get Dimo sensor data from DIMO_SENSORS defs."""
        for key, sensor_def in DIMO_SENSORS.items():
            if hasattr(self.client, sensor_def.value_fn):
                fn = getattr(self.client, sensor_def.value_fn)
                self.dimo_data[key] = await self.hass.async_add_executor_job(fn)

    async def get_vehicles_data(self):
        """Get all vehicle data."""
        vehicles_data = await self.get_api_data(
            self.client.get_all_vehicles_for_license, self.entry.data[CONF_CLIENT_ID]
        )
        if vehicles_data is None:
            _LOGGER.warning("Got no data from the API. Skipping update")
            return

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
            available_signals_data = await self.get_api_data(
                self.client.get_available_signals, vehicle_token_id
            )

            if available_signals_data is None:
                _LOGGER.warning("Got no data from the API. Skipping update")
                return

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
            signals_data = await self.get_api_data(
                self.client.get_latest_signals,
                vehicle_token_id,
                self.vehicle_data[vehicle_token_id].available_signals,
            )

            if signals_data is None:
                _LOGGER.warning("Got no data from the API. Skipping update")
                return

            _LOGGER.debug("SIGNALS DATA: %s", signals_data)
            self.vehicle_data[vehicle_token_id].signal_data = get_key(
                "data.signalsLatest", signals_data
            )
            self.vehicle_data[vehicle_token_id].signal_data_errors = get_key(
                "errors", signals_data
            )

            # Fetch and store token rewards
            await self._update_token_rewards(vehicle_token_id)
        else:
            _LOGGER.error(
                "Unable to fetch signals data for %s.  Not a known vehicle on this account",
                vehicle_token_id,
            )

    @staticmethod
    def _get_current_timestamp():
        """Get the current UTC timestamp in ISO 8601 format."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    async def _get_vehicle_vin(self, vehicle_token_id: str):
        """Retrieve VIN for a vehicle"""
        _LOGGER.debug("Retrieving VIN for %s", vehicle_token_id)
        try:
            vin = await self.get_api_data(self.client.get_vin, vehicle_token_id)
            if vin:
                self.vehicle_data[vehicle_token_id].vin = vin

        except Exception as e:
            _LOGGER.error("Error getting VIN for vehicle %s: %s", vehicle_token_id, e)

    async def _update_token_rewards(self, vehicle_token_id: str):
        """Fetch and update token rewards for a vehicle."""
        try:
            rewards_data = await self.get_api_data(
                self.client.get_rewards_for_vehicle,
                vehicle_token_id,
            )
            if rewards_data:
                timestamp = self._get_current_timestamp()
                earnings = rewards_data["data"]["vehicle"]["earnings"]["totalTokens"]
                self.vehicle_data[vehicle_token_id].signal_data["tokenRewards"] = {
                    "timestamp": timestamp,
                    "value": earnings,
                }
        except KeyError:
            _LOGGER.warning(
                "Rewards data structure unexpected for vehicle %s.", vehicle_token_id
            )
        except Exception as e:
            _LOGGER.error(
                "Error fetching token rewards for vehicle %s: %s", vehicle_token_id, e
            )

    async def async_update_data(self):
        """Update data from api."""
        _LOGGER.debug("Updating from the DIMO api")
        tasks = [self.get_dimo_sensor_data()]
        tasks.extend(
            self.get_signals_data_for_vehicle(token_id)
            for token_id in self.vehicle_data
        )
        await asyncio.gather(*tasks)
        return True

    async def get_api_data(self, target, *args) -> dict[str, Any] | None:
        """Request data from api."""
        try:
            return await self.hass.async_add_executor_job(target, *args)
        except InvalidClientIdError:
            _LOGGER.error(
                "Unable to retreive data from the Dimo api due to an invalid client id"
            )
            raise
        except InvalidApiKeyFormat:
            _LOGGER.error(
                "Unable to retreive data from the Dimo api due to an invalid api key"
            )
            raise
        except NoVehiclesException:
            _LOGGER.error(
                "No vehicles exist on this account.  Please check your vehicle sharing in the Dimo app"
            )
            raise
        except ConnectionResetError as ex:  # Non-critical exceptions.
            _LOGGER.warn("DIMO API request error: %s", ex)
            return None
        except Exception as ex:  # noqa: BLE001
            _LOGGER.error(
                "An unknown error occurred trying to retrieve data from the Dimo api.  Error is: %s",
                ex,
            )
            raise

    def create_dimo_device(self):
        """Create device for Dimo sensors."""
        device_registry = dr.async_get(self.hass)
        device_registry.async_get_or_create(
            config_entry_id=self.entry.entry_id,
            identifiers={(DOMAIN, DOMAIN)},
            manufacturer="DIMO",
            name="DIMO",
            model="DIMO",
        )

    def create_vehicle_device(self, vehicle_token_id: str):
        """Create device for vehicle."""
        vehicle = self.vehicle_data[vehicle_token_id]

        # Build a set of identifiers for the vehicle device
        # including vin, if available

        identifiers = {(DOMAIN, vehicle_token_id)}
        if vehicle.vin:
            _LOGGER.debug("Got vin for %s", vehicle_token_id)
            identifiers.add((DOMAIN, vehicle.vin))

        device_registry = dr.async_get(self.hass)
        device_registry.async_get_or_create(
            config_entry_id=self.entry.entry_id,
            identifiers=identifiers,
            manufacturer=vehicle.definition["make"],
            name=f"{vehicle.definition["make"]} {vehicle.definition["model"]}",
            model=vehicle.definition["model"],
        )
