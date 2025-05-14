"""Helper functions."""

from collections.abc import Mapping
from typing import Any
import logging

_LOGGER = logging.getLogger(__name__)


def get_key(
    path: str, data: Mapping[str, Any]
) -> dict[str, dict | str | int] | str | int:
    """Try to get a deep value from a dict based on a dot-notation."""
    if not path:
        return None

    current: Any = data
    for key in path.split("."):
        if isinstance(current, Mapping) and key in current:
            current = current[key]
        else:
            _LOGGER.debug("get_key: path %r failed at segment %r", path, key)
            return None

    return current
