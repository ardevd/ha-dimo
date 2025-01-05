import logging
from typing import Optional
from .auth import Auth
from .queries import (
    GET_VEHICLE_REWARDS_QUERY,
    GET_AVAILABLE_SIGNALS_QUERY,
    GET_LATEST_SIGNALS_QUERY,
    GET_ALL_VEHICLES_QUERY,
)
from dimo.graphql import Telemetry

_LOGGER = logging.getLogger(__name__)


class DimoClient:
    def __init__(self, auth: Auth):
        self.auth = auth
        self.dimo = auth.get_dimo()

    def init(self) -> None:
        """Initialize the client by retrieving an authorization token"""
        try:
            self.auth.get_access_token()
        except Exception as e:
            _LOGGER.error(f"Failed to init Dimo client: {e}")
            raise

    def _fetch_privileged_token(self, token_id: str) -> str:
        """Retrieve privileged token for specified token id"""
        try:
            return self.auth.get_privileged_token(token_id)
        except Exception as e:
            _LOGGER.error(f"Failed to obtain privileged token for {token_id}: {e}")
            raise

    def get_vehicle_makes(self):
        return self.dimo.device_definitions.list_device_makes()

    def lock_doors(self, token_id: str):
        priv_token = self._fetch_privileged_token(token_id)
        return self.dimo.devices.lock_doors(priv_token, token_id)

    def unlock_doors(self, token_id: str):
        priv_token = self._fetch_privileged_token(token_id)
        return self.dimo.devices.unlock_doors(priv_token, token_id)

    def get_rewards_for_vehicle(self, token_id: str):
        """Get total token rewards generated by vehicle"""
        query = GET_VEHICLE_REWARDS_QUERY.format(token_id=token_id)
        return self.dimo.identity.query(query)

    def get_available_signals(self, token_id: str):
        """Get list of available signals for a specified vehicle"""
        priv_token = self._fetch_privileged_token(token_id)
        query = GET_AVAILABLE_SIGNALS_QUERY.format(token_id=token_id)
        return self.dimo.telemetry.query(query, priv_token)

    def get_latest_signals(self, token_id, signal_names: list[str]):
        """Get the latest signal values for the specified vehicle"""
        priv_token = self._fetch_privileged_token(token_id)
        signals_query = "\n".join(
            [
                f"{signal_name} {{\n  timestamp\n  value\n}}"
                for signal_name in signal_names
            ]
        )

        query = GET_LATEST_SIGNALS_QUERY.format(
            token_id=token_id, signals=signals_query
        )
        return self.dimo.telemetry.query(query, priv_token)

    def get_all_vehicles_for_license(self, license_id=None):
        """List all vehicles for the specified license."""
        if license_id is None:
            license_id = self.auth.client_id

        query = GET_ALL_VEHICLES_QUERY.format(license_id=license_id)
        return self.dimo.identity.query(query)

    def get_total_dimo_vehicles(self) -> Optional[int]:
        """
        Get the total number of vehicles on DIMO.

        :return: Total count of vehicles or None if failed.
        """
        try:
            result = self.dimo.identity.count_dimo_vehicles()
            return result.get("data", {}).get("vehicles", {}).get("totalCount")
        except Exception as e:
            _LOGGER.error(f"Failed to get total DIMO vehicles: {e}")
            return None

    def get_vin(self, token_id) -> str:
        """
        Retrieve VIN for the specified token_id
        """
        vehicle_jwt = self._fetch_privileged_token(token_id)
        return self.dimo.telemetry.get_vin(vehicle_jwt, token_id)
