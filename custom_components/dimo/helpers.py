"""Helper functions."""

from typing import Any


def get_key(path: str, data: Any, default: Any = None) -> Any:
    """
    Get a value from a nested structure (dict/list) using dot-notation.

    Args:
        path: The dotted path to traverse (e.g. "data.vehicles.0.id").
        data: The root object to search (dict or list).
        default: The value to return if the path is invalid or not found.

    Returns:
        The found value or the default.
    """
    if not path:
        return default

    current = data
    for segment in path.split("."):
        # Handle Dictionaries
        if isinstance(current, dict) and segment in current:
            current = current[segment]
            continue

        # Handle Lists (via integer index)
        if isinstance(current, list):
            try:
                index = int(segment)
                if 0 <= index < len(current):
                    current = current[index]
                    continue
            except ValueError:
                pass  # Segment was not an integer

        # If we reach here, traversal failed
        return default

    return current
