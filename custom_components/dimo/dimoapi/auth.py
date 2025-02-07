from dataclasses import dataclass, field
import requests
import dimo as dimo_api
from datetime import datetime, timezone
from typing import Optional
import jwt
import logging

_LOGGER = logging.getLogger(__name__)


@dataclass
class AuthToken:
    """Class to hold JWT based authentication tokens."""

    token: str
    expiration: float = field(init=False)

    def __post_init__(self):
        decoded_token = jwt.decode(
            self.token,
            options={"verify_signature": False},
        )
        self.expiration = decoded_token.get("exp", 0.0)


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
        self.access_token = None
        self.privileged_tokens: dict[str, AuthToken] = {}
        self.dimo = dimo if dimo else dimo_api.DIMO("Production")

    def get_privileged_token(
        self, vehicle_token_id: str, permissions: Optional[list]
    ) -> AuthToken:
        """Get privileged token from DIMO token exchange API"""
        if not self.privileged_tokens.get(
            vehicle_token_id
        ) or self._is_privileged_token_expired(vehicle_token_id):
            if permissions is None:
                _LOGGER.debug("No permissions specified. Fallback to default")
                permissions = [1, 2, 3, 4, 5, 6]
            _LOGGER.debug(
                f"Obtaining privileged token for {vehicle_token_id} with privileges {permissions}"
            )
            token = self.dimo.token_exchange.exchange(
                self.access_token.token,
                privileges=permissions,
                token_id=vehicle_token_id,
            )["token"]

            self.privileged_tokens[vehicle_token_id] = AuthToken(token)

        return self.privileged_tokens[vehicle_token_id]

    def _is_jwt_token_expired(self, token: AuthToken) -> bool:
        """Assert jwt token expiration"""
        exp = token.expiration
        expiration_time = datetime.fromtimestamp(exp, timezone.utc)
        current_time = datetime.now(timezone.utc)

        return current_time > expiration_time

    def _is_privileged_token_expired(self, vehicle_token_id: str) -> bool:
        """Assert privileged token expiration."""
        if self.privileged_tokens.get(vehicle_token_id):
            return self._is_jwt_token_expired(
                self.privileged_tokens.get(vehicle_token_id)
            )

        return True

    def _get_auth(self):
        _LOGGER.debug("Retrieving access token")
        try:
            auth_header = self.dimo.auth.get_token(
                client_id=self.client_id,
                domain=self.domain,
                private_key=self.private_key,
            )
            self.access_token = AuthToken(auth_header["access_token"])
            _LOGGER.debug("access token retrieved")
        except requests.exceptions.HTTPError as e:
            if "404" in str(e):
                raise InvalidClientIdError from e
            if "400" in str(e):
                raise InvalidCredentialsError from e
            raise  # Re-raise for unexpected errors

        except ValueError as e:
            raise InvalidApiKeyFormat from e

    def get_access_token(self) -> AuthToken:
        """
        Get the DIMO API access token.
        Will obtain a fresh token if no token exists or if
        the current token is expired
        """
        if self.access_token is None or self._is_jwt_token_expired(self.access_token):
            self._get_auth()
        return self.access_token

    def get_dimo(self):
        """
        Return current DIMO api instance
        """
        return self.dimo


class InvalidClientIdError(Exception):
    """ClientID value is invalid or unknown."""


class InvalidCredentialsError(Exception):
    """Provided credentials are not correct."""


class InvalidApiKeyFormat(Exception):
    """API key format is invalid."""
