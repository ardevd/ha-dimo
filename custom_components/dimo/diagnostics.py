"""Diagnostics support for Dimo."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntry

from . import DIMOConfigEntry


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return _async_get_diagnostics(hass, entry)


@callback
def _async_get_diagnostics(
    hass: HomeAssistant,
    entry: DIMOConfigEntry,
    device: DeviceEntry | None = None,
) -> dict[str, Any]:
    coordinator = entry.runtime_data.coordinator
    return [
        {token_id: vehicle_data.__dict__}
        for token_id, vehicle_data in coordinator.vehicle_data.items()
    ]
