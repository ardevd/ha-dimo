GET_VEHICLE_REWARDS_QUERY = """
query GetVehicleRewardsByTokenId {{
  vehicle(tokenId: {token_id}) {{
      earnings {{
        totalTokens
      }}
    }}
}}
"""

GET_AVAILABLE_SIGNALS_QUERY = """
query AvailableSignals {{
  availableSignals(tokenId: {token_id})
}}
"""

GET_LATEST_SIGNALS_QUERY = """
query {{
  signalsLatest(tokenId: {token_id}) {{
    {signals}
  }}
}}
"""

GET_ALL_VEHICLES_QUERY = """
query VehiclesForLicense {{
  vehicles(filterBy: {{ privileged: "{license_id}" }}, first: 100) {{
    nodes {{
      syntheticDevice {{ id }}
      tokenId
      definition {{ make model year }}
    }}
    totalCount
  }}
}}
"""

CHECK_SACD_QUERY = """
  query CheckSACD {{
  vehicle(tokenId: {token_id}) {{
    sacds(first:100) {{
      nodes {{
        permissions
        grantee
      }}
    }}
  }}
}}
"""
