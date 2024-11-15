from loguru import logger
from .auth import Auth


class DimoClient:
    def __init__(self, auth: Auth):
        self.auth = auth
        self.dimo = auth.get_dimo()

    def init(self):
        self.auth.get_token()

    def get_vehicle_makes(self):
        return self.dimo.device_definitions.list_device_makes()

    def get_available_signals(self, token_id):
        priv_token = self.auth.get_privileged_token(token_id)
        query = f"""
    query {{
      availableSignals(
        tokenId: {token_id}
      )
    }}
    """
        return self.dimo.telemetry.query(query, priv_token["token"])

    def get_latest_signals(self, token_id, signal_names: list[str]):
        logger.debug(f"Querying API for {len(signal_names)} signals")
        priv_token = self.auth.get_privileged_token(token_id)
        signals_query = "\n".join(
            [
                f"{signal_name} {{\n  timestamp\n  value\n}}"
                for signal_name in signal_names
            ]
        )
        query = f"""
        query {{
            signalsLatest(tokenId: {token_id}) {{
                {signals_query}
            }}
        }}
        """
        return self.dimo.telemetry.query(query, priv_token["token"])

    def get_all_vehicles_for_license(self, license_id: str):
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
        return self.dimo.identity.query(query=query_all_vehicles)
