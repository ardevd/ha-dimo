import asyncio
from ha_dimo.dimo_client import DimoClient
from ha_dimo.auth import Auth

client_id = "0x7D076b943E4dA88C39D51f8c9b03f79b27037bc8"
domain = "https://www.google.com"
private_key = "0xbbe903286eb1e0e2bc5cf39ac6734f170b04665bb8b281f188942e7c3f541981"

auth = Auth(client_id, domain, private_key)
asyncio.run(auth.get_token())

