from homeassistant import config_entries, setup
from custom_components.dimo.const import DOMAIN


async def test_flow_user_step_no_input(hass):
    """Test creating the flow with no user input."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == "form"
    # At this stage, no user input was provided so it just shows the form
