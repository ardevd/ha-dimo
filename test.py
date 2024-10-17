import asyncio
from dimo import DIMO
from loguru import logger

async def get_auth():
    dimo = DIMO("Production")
    auth_header = await dimo.auth.get_token(client_id="0x7D076b943E4dA88C39D51f8c9b03f79b27037bc8", 
                                            domain="https://www.google.com", 
                                            private_key="bbe903286eb1e0e2bc5cf39ac6734f170b04665bb8b281f188942e7c3f541981")
    access_token = auth_header["access_token"]
    return access_token

logger.info("Retrieving access token")
access_token = asyncio.run(get_auth())
logger.debug("access token: {access_token}", access_token=access_token)
