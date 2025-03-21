from attr import dataclass
import logging
from dataclasses import dataclass
from typing import Optional
from .auth import Auth
from .queries import (
    GET_VEHICLE_REWARDS_QUERY,
    GET_AVAILABLE_SIGNALS_QUERY,
    GET_LATEST_SIGNALS_QUERY,
    GET_ALL_VEHICLES_QUERY,
)

_LOGGER = logging.getLogger(__name__)


@dataclass
class VehicleSharingPermission:
    """SACD permission model class"""

    client_id: str
    privileges: list


class DimoClient:
    def __init__(self, auth: Auth, permission_checker=None):
        self.auth = auth
        self.dimo = auth.get_dimo()
        self.permission_checker = permission_checker or self._check_sacd_permissions

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
            # Assert access token validity
            self.auth.get_access_token()
            # Get privileged token with the granted permissions
            permissions = self.permission_checker(token_id)
            return self.auth.get_privileged_token(
                token_id, permissions.privileges
            ).token
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
        if signal_names is None:
            signal_names = []

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
        except ConnectionError as ex:
            _LOGGER.warn(
                "DIMO API request error when retrieving DIMO vehicle count %s", ex
            )
            return None
        except Exception as e:
            _LOGGER.error(f"Failed to get total DIMO vehicles: {e}")
            return None

    def _check_sacd_permissions(self, token_id) -> Optional[VehicleSharingPermission]:
        """
        Get Service Access Contract Definition details for a given vehicle,
        including which clients the vehicle has been shared with and
        with what permissions
        """
        result = self.dimo.identity.check_vehicle_privileges(token_id)
        permissions_dict = result["data"]["vehicle"]["sacds"]["nodes"]

        for perm in permissions_dict:
            grantee = perm["grantee"]
            if grantee == self.auth.client_id:
                return VehicleSharingPermission(
                    grantee, hex_to_permissions(perm["permissions"])
                )

        return None

    def get_vin(self, token_id) -> Optional[str]:
        """
        Retrieve the Vehicle Identification Number (VIN) for the specified token ID.

        :param token_id: Token ID associated with the vehicle.
        :return: The VIN as a string, or None if unavailable.
        """
        try:
            vehicle_jwt = self._fetch_privileged_token(token_id)
            vin_response = self.dimo.telemetry.get_vin(vehicle_jwt, token_id)
            vin = vin_response.get("data", {}).get("vinVCLatest", {}).get("vin")
            if vin:
                _LOGGER.debug(
                    f"Successfully retrieved VIN for token_id {token_id}: {vin}"
                )
                return vin
            _LOGGER.warning(
                f"VIN not found in response for token_id {token_id}: {vin_response}"
            )
            return None
        except KeyError as e:
            _LOGGER.error(
                f"Malformed response when retrieving VIN for token_id {token_id}: {e}"
            )
            return None
        except Exception as e:
            _LOGGER.error(f"Failed to retrieve VIN for token_id {token_id}: {e}")
            return None


def hex_to_permissions(hex_value):
    """
    Convert a hex–encoded permission value into a list of permission levels.
    """
    num = int(hex_value, 0)
    num >>= 2

    bin_str = bin(num)[2:]

    # Ensure an even number of bits by padding with a leading zero if needed.
    if len(bin_str) % 2 != 0:
        bin_str = "0" + bin_str

    permissions = []
    group_count = len(bin_str) // 2

    # Process each group from right to left.
    # The right–most group corresponds to permission level 1, the next to level 2, etc.
    for i in range(group_count):
        start = len(bin_str) - 2 * (i + 1)
        end = len(bin_str) - 2 * i
        group = bin_str[start:end]
        # If the 2–bit group is nonzero, the permission is granted.
        if int(group, 2) != 0:
            permissions.append(i + 1)

    return permissions
