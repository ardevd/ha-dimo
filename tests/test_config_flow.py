import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.dimo.config_flow import InvalidAuth
from custom_components.dimo.const import (CONF_AUTH_PROVIDER, CONF_LICENSE_ID,
                                          CONF_PRIVATE_KEY, DOMAIN, CONF_POLL_INTERVAL,
                                          DEFAULT_POLL_INTERVAL)


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Use enable_custom_integrations in this module."""
    yield


async def test_flow_user_step_no_input(hass):
    """Test creating the flow with no user input."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )
    assert result["type"] == "form"
    # At this stage, no user input was provided so it just shows the form


async def test_flow_invalid_auth(hass, monkeypatch):
    """Test the flow when invalid credentials are provided."""

    async def mock_validate_input(hass, data):
        raise InvalidAuth

    monkeypatch.setattr(
        "custom_components.dimo.config_flow.validate_input", mock_validate_input
    )

    user_input = {
        CONF_LICENSE_ID: "dummy_client",
        CONF_AUTH_PROVIDER: "dummy_provider",
        CONF_PRIVATE_KEY: "dummy_private",
    }

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}, data=user_input
    )

    assert result["type"] == "form"
    assert result["errors"]["base"] == "invalid_auth"


async def test_flow_valid_input(hass, monkeypatch):
    """Test a successful config flow."""

    async def mock_validate_input(hass, data):
        return {"title": "DIMO"}

    monkeypatch.setattr(
        "custom_components.dimo.config_flow.validate_input", mock_validate_input
    )

    user_input = {
        CONF_LICENSE_ID: "dummy_client",
        CONF_AUTH_PROVIDER: "dummy_provider",
        CONF_PRIVATE_KEY: "dummy_private",
    }

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}, data=user_input
    )

    assert result["type"] == "create_entry"
    assert result["title"] == "DIMO"
    assert result["data"] == user_input


async def test_options_flow_init_default_values(hass, monkeypatch):
    """Test options flow initialization with default poll interval."""
    # Mock validate_input to allow creating a config entry
    async def mock_validate_input(hass, data):
        return {"title": "DIMO"}

    monkeypatch.setattr(
        "custom_components.dimo.config_flow.validate_input", mock_validate_input
    )

    user_input = {
        CONF_LICENSE_ID: "dummy_client",
        CONF_AUTH_PROVIDER: "dummy_provider",
        CONF_PRIVATE_KEY: "dummy_private",
    }

    # Create a config entry first
    config_result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}, data=user_input
    )
    assert config_result["type"] == "create_entry"
    
    # Get the created config entry
    config_entry = hass.config_entries.async_entries(DOMAIN)[0]
    
    # Initialize the options flow
    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    
    assert result["type"] == "form"
    assert result["step_id"] == "init"
    # Verify the schema contains the poll interval field
    schema_keys = [str(key) for key in result["data_schema"].schema.keys()]
    assert any(CONF_POLL_INTERVAL in key for key in schema_keys)


async def test_options_flow_update_poll_interval(hass, monkeypatch):
    """Test updating poll interval through options flow."""
    # Mock validate_input to allow creating a config entry
    async def mock_validate_input(hass, data):
        return {"title": "DIMO"}

    monkeypatch.setattr(
        "custom_components.dimo.config_flow.validate_input", mock_validate_input
    )

    user_input = {
        CONF_LICENSE_ID: "dummy_client",
        CONF_AUTH_PROVIDER: "dummy_provider",
        CONF_PRIVATE_KEY: "dummy_private",
    }

    # Create a config entry first
    config_result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}, data=user_input
    )
    assert config_result["type"] == "create_entry"
    
    # Get the created config entry
    config_entry = hass.config_entries.async_entries(DOMAIN)[0]
    
    # Start the options flow
    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    
    assert result["type"] == "form"
    
    # Submit a new poll interval value
    new_poll_interval = 60
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={CONF_POLL_INTERVAL: new_poll_interval}
    )
    
    assert result["type"] == "create_entry"
    assert result["data"][CONF_POLL_INTERVAL] == new_poll_interval


async def test_options_flow_triggers_reload(hass, monkeypatch):
    """Test that updating options triggers a config entry reload."""
    # Mock validate_input to allow creating a config entry
    async def mock_validate_input(hass, data):
        return {"title": "DIMO"}

    monkeypatch.setattr(
        "custom_components.dimo.config_flow.validate_input", mock_validate_input
    )

    user_input = {
        CONF_LICENSE_ID: "dummy_client",
        CONF_AUTH_PROVIDER: "dummy_provider",
        CONF_PRIVATE_KEY: "dummy_private",
    }

    # Create a config entry first
    config_result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}, data=user_input
    )
    assert config_result["type"] == "create_entry"
    
    # Get the created config entry
    config_entry = hass.config_entries.async_entries(DOMAIN)[0]
    
    # Mock the async_reload to track if it's called
    with patch("custom_components.dimo.async_update_options") as mock_update_options:
        
        # Add the update listener to simulate the integration setup
        config_entry.add_update_listener(mock_update_options)
        
        # Start and complete the options flow
        result = await hass.config_entries.options.async_init(config_entry.entry_id)
        
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            user_input={CONF_POLL_INTERVAL: 60}
        )
        
        assert result["type"] == "create_entry"
        
        # Wait for the update listener to be called
        await hass.async_block_till_done()
        
        # Verify that the update listener was called
        mock_update_options.assert_called_once()
