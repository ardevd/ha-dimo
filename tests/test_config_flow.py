from custom_components.dimo.const import (
    DOMAIN,
    CONF_LICENSE_ID,
    CONF_AUTH_PROVIDER,
    CONF_PRIVATE_KEY,
)

from custom_components.dimo.config_flow import InvalidAuth
import pytest


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
