from dataclasses import dataclass
import requests
import dimo as dimo_api
from datetime import datetime, timezone
from typing import Optional
import jwt
import logging

_LOGGER = logging.getLogger(__name__)


@dataclass
class PrivilegedToken:
    """Class to hold privileged tokens."""

    token: str


class Auth:
    """Wrapper for the DIMO SDK authentication related features"""

    def __init__(
        self,
        client_id: str,
        domain: str,
        private_key: str,
        dimo: Optional[dimo_api.DIMO] = None,
    ) -> None:
        """
        Initialize the authentication wrapper for the DIMO API.
        """
        self.client_id = client_id
        self.domain = domain
        self.private_key = private_key
        self.token = None
        self.privileged_tokens: dict[str, PrivilegedToken] = {}
        self.dimo = dimo if dimo else dimo_api.DIMO("Production")

    def get_privileged_token(self, vehicle_token_id: str) -> str:
        """Get privileged token from DIMO token exchange API"""
        if not self.privileged_tokens.get(
            vehicle_token_id
        ) or self._is_privileged_token_expired(vehicle_token_id):
            _LOGGER.debug(f"Obtaining privileged token for {vehicle_token_id}")
            token = self.dimo.token_exchange.exchange(
                self.token, privileges=[1, 2, 3, 4], token_id=vehicle_token_id
            )

            self.privileged_tokens[vehicle_token_id] = PrivilegedToken(token)

        return self.privileged_tokens[vehicle_token_id].token

    def _is_privileged_token_expired(self, vehicle_token_id: str) -> bool:
        """Assert privileged token expiration."""
        if self.privileged_tokens.get(vehicle_token_id):
            decoded_token = jwt.decode(
                self.privileged_tokens[vehicle_token_id].token["token"],
                options={"verify_signature": False},
            )
            exp = decoded_token.get("exp")
            if exp:
                expiration_time = datetime.fromtimestamp(exp, timezone.utc)
                current_time = datetime.now(timezone.utc)

                return current_time > expiration_time
        return True

    def _get_auth(self):
        _LOGGER.debug("Retrieving access token")
        try:
            auth_header = self.dimo.auth.get_token(
                client_id=self.client_id,
                domain=self.domain,
                private_key=self.private_key,
            )
            self.token = auth_header["access_token"]
            _LOGGER.debug("access token retrieved")
        except requests.exceptions.HTTPError as e:
            if "404" in str(e):
                raise InvalidClientIdError from e
            if "400" in str(e):
                raise InvalidCredentialsError from e
            raise  # Re-raise for unexpected errors

        except ValueError as e:
            raise InvalidApiKeyFormat from e

    def get_token(self):
        if self.token is None:
            self._get_auth()
        return self.token

    def get_dimo(self):
        return self.dimo


class InvalidClientIdError(Exception):
    """ClientID value is invalid or unknown."""


class InvalidCredentialsError(Exception):
    """Provided credentials are not correct."""


class InvalidApiKeyFormat(Exception):
    """API key format is invalid."""
