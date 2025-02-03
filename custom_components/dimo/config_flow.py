"""Config flow for DIMO integration."""

from __future__ import annotations

import logging
from typing import Any

import requests
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_CLIENT_ID
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import CONF_AUTH_PROVIDER, CONF_PRIVATE_KEY, DOMAIN
from .dimoapi import (
    Auth,
    DimoClient,
    InvalidApiKeyFormat,
    InvalidClientIdError,
    InvalidCredentialsError,
)
from .helpers import get_key

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_CLIENT_ID): str,
        vol.Required(CONF_AUTH_PROVIDER): str,
        vol.Required(
            CONF_PRIVATE_KEY,
        ): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""

    try:
        auth = Auth(
            data[CONF_CLIENT_ID], data[CONF_AUTH_PROVIDER], data[CONF_PRIVATE_KEY]
        )
        client = DimoClient(auth)
        await hass.async_add_executor_job(client.init)
        _LOGGER.debug("Token retrieved")
        # Get list of vehicles on account and return for next step
        vehicles_data = await hass.async_add_executor_job(
            client.get_all_vehicles_for_license, data[CONF_CLIENT_ID]
        )
        if vehicles_data:
            if vehicles := get_key("data.vehicles.nodes", vehicles_data):
                _LOGGER.debug("CF Vehicles: %s", vehicles)
                return {"title": "DIMO"}
        raise NoVehiclesException  # noqa: TRY301
    except InvalidCredentialsError as ex:
        raise InvalidAuth from ex
    except requests.exceptions.HTTPError as ex:
        raise CannotConnect from ex


class ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for DIMO."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except InvalidClientIdError:
                errors["base"] = "invalid_client_id"
            except InvalidApiKeyFormat:
                errors["base"] = "invalid_api_key"
            except NoVehiclesException:
                errors["base"] = "no_vehicles"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


class NoVehiclesException(HomeAssistantError):
    """Error to indicate no vehicles on the account."""
