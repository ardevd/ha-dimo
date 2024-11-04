import asyncio
from loguru import logger
from .auth import Auth

class DimoClient:
    def __init__(self, auth: Auth):
        self.auth = auth
        self.dimo = auth.get_dimo()

    async def init(self):
        await self.auth.get_token()

    async def get_vehicle_makes(self):
        return await self.dimo.device_definitions.list_device_makes()
