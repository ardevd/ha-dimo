from datetime import datetime, timedelta, timezone

import jwt

from custom_components.dimo.dimoapi.auth import AuthToken


def create_mock_token(exp_offset) -> AuthToken:
    """
    Helper function to create a mock JWT token with a specific expiration offset.
    """
    expiration_time = datetime.now(timezone.utc) + timedelta(seconds=exp_offset)
    payload = {"exp": expiration_time.timestamp()}
    return AuthToken(jwt.encode(payload, "secret", algorithm="HS256"))
