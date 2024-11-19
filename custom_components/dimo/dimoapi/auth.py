import requests
import dimo as dimo_api
import time
from loguru import logger


class Auth:
    """Wrapper for the DIMO SDK authentication related features"""

    class InvalidClientIdError(Exception):
        """ClientID value is invalid or unknown"""

        pass

    class InvalidCredentialsError(Exception):
        """Provided credentials are not correct"""

        pass

    class InvalidApiKeyFormat(Exception):
        """API key format is invalid"""

        pass

    def __init__(self, client_id, domain, private_key, dimo=None):
        self.client_id = client_id
        self.domain = domain
        self.private_key = private_key
        self.token = None
        self.privileged_token = None
        self.privileged_token_expiry = None
        self.dimo = dimo if dimo else dimo_api.DIMO("Production")

    def get_privileged_token(self, vehicle_token_id):
        if not self.privileged_token or self._is_privileged_token_expired():
            logger.debug("Obtaining privileged token")
            self.privileged_token = self.dimo.token_exchange.exchange(
                self.token, privileges=[1, 2, 3, 4], token_id=vehicle_token_id
            )
            self.privileged_token_expiry = time.time() + 600
            logger.debug("New privileged token obtained")

        return self.privileged_token

    def _is_privileged_token_expired(self):
        """Assert privileged token expiration"""
        return (
            not self.privileged_token_expiry
            or time.time() >= self.privileged_token_expiry
        )

    def _get_auth(self):
        logger.debug("Retrieving access token")
        try:
            auth_header = self.dimo.auth.get_token(
                client_id=self.client_id,
                domain=self.domain,
                private_key=self.private_key,
            )
            self.token = auth_header["access_token"]
            logger.debug("access token retrieved")
        except requests.exceptions.HTTPError as e:
            if "404" in str(e):
                raise self.InvalidClientIdError
            elif "400" in str(e):
                raise self.InvalidCredentialsError
            else:
                raise  # Re-raise for unexpected errors

        except ValueError as e:
            raise self.InvalidApiKeyFormat

    def get_token(self):
        if self.token is None:
            self._get_auth()
        return self.token

    def get_dimo(self):
        return self.dimo
