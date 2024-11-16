"""Helper functions."""

from functools import reduce
import logging

_LOGGER = logging.getLogger(__name__)


def get_key(
    dot_notation_path: str,
    data: dict,
) -> dict[str, dict | str | int] | str | int:
    """Try to get a deep value from a dict based on a dot-notation."""
    if dot_notation_path is None:
        return None

    try:
        return reduce(dict.get, dot_notation_path.split("."), data)
    except (TypeError, KeyError) as ex:
        _LOGGER.error("TYPE ERROR: %s - %s", dot_notation_path, ex)
        return None
