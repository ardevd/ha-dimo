import asyncio
import dimo as dimo_api
from loguru import logger


class Auth:
    def __init__(self, client_id, domain, private_key, dimo=None):
        self.client_id = client_id
        self.domain = domain
        self.private_key = private_key
        self.token = None
        self.dimo = dimo if dimo else dimo_api.DIMO("Production")

    def get_privileged_token(self, vehicle_token_id):
        logger.debug("Obtaining privileged token")
        return self.dimo.token_exchange.exchange(
            self.token, privileges=[1, 3], token_id=vehicle_token_id
        )

    def _get_auth(self):
        logger.debug("Retrieving access token")
        auth_header = self.dimo.auth.get_token(
            client_id=self.client_id,
            domain=self.domain,
            private_key=self.private_key,
        )
        self.token = auth_header["access_token"]
        logger.debug("access token retrieved")

    def get_token(self):
        if self.token is None:
            self._get_auth()
        return self.token

    def get_dimo(self):
        return self.dimo
