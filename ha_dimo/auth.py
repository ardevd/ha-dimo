import asyncio
from dimo import DIMO
from loguru import logger


class Auth:
    def __init__(self, client_id, domain, private_key):
        self.client_id = client_id
        self.domain = domain
        self.private_key = private_key
        self.token = None
        

    async def get_auth(self):
        logger.info("Retrieving access token")
        dimo = DIMO("Production")
        auth_header = await dimo.auth.get_token(
            client_id=self.client_id,
            domain=self.domain,
            private_key=self.private_key,
        )
        self.token = auth_header["access_token"]
        logger.debug(f"access token: {self.token}")
        
    async def get_token(self):
        if self.token is None:
            await self.get_auth()
        return self.token

