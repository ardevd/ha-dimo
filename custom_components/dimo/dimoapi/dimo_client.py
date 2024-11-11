import asyncio
from loguru import logger
from auth import Auth

class DimoClient:
    def __init__(self, auth: Auth):
        self.auth = auth
        self.dimo = auth.get_dimo()
        
    async def init(self):
        await self.auth.get_token()

    async def get_vehicle_makes(self):
        return await self.dimo.device_definitions.list_device_makes()

    async def get_available_signals(self, token_id):
        priv_token = await self.auth.get_privileged_token(token_id)
        query = f"""
    query {{
      availableSignals(
        tokenId: {token_id}
      )
    }}
    """
        return await self.dimo.telemetry.query(query, priv_token)
        
    async def get_all_vehicles_for_license(self, license_id: str):
        query_all_vehicles = f"""
    query {{
      vehicles(filterBy: {{ privileged: "{license_id}" }}, first: 100) {{
        nodes {{
          syntheticDevice {{
            id
          }}
          tokenId
          definition {{
            make
            model
            year
          }}
        }},
        totalCount
      }}
    }}
    """
        return await self.dimo.identity.query(query=query_all_vehicles)

