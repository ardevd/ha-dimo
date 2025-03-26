from custom_components.dimo.const import DOMAIN
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
