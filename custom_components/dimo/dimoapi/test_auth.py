import pytest
from unittest.mock import AsyncMock, Mock
from dimo_client import DimoClient
from auth import Auth

@pytest.mark.asyncio
async def test_auth_get_token(mocker):
    fake_token = "abcdef1234"
    # Mocking the DIMO instance and auth.get_token
    dimo_mock = Mock()
    dimo_mock.auth.get_token = AsyncMock(return_value={"access_token": fake_token})
    
    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)

    # Test token retrieval
    token = await auth.get_token()
    
    assert token == fake_token
    dimo_mock.auth.get_token.assert_called_once_with(
        client_id="client_id",
        domain="domain",
        private_key="private_key"
    )

@pytest.mark.asyncio
async def test_dimo_client_get_vehicle_makes(mocker):
    # Mocking DIMO instance and list_device_makes
    dimo_mock = Mock()
    dimo_mock.device_definitions.list_device_makes = AsyncMock(return_value=["Land Rover", "BMW"])
    
    auth = Auth("client_id", "domain", "private_key", dimo=dimo_mock)
    client = DimoClient(auth)
    
    # Test get_vehicle_makes
    makes = await client.get_vehicle_makes()

    assert makes == ["Land Rover", "BMW"]
    dimo_mock.device_definitions.list_device_makes.assert_called_once()
