import asyncio
from dimo import DIMO
from loguru import logger
from .auth import Auth

class DimoClient:
    def __init__(self, auth: Auth):
        self.auth = auth

    async def test(self):
        token = await self.auth.get_token()
        print(token)
