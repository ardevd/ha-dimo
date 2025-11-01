import pytest

from custom_components.dimo.helpers import get_key  # Replace 'helpers' with your actual module name


def test_simple_key():
    data = {"a": 1, "b": "foo"}
    assert get_key("a", data) == 1
    assert get_key("b", data) == "foo"


def test_nested_keys():
    data = {"a": {"b": {"c": 42}}}
    assert get_key("a.b.c", data) == 42


def test_missing_key_returns_none():
    data = {"a": 1}
    # Missing leaf
    assert get_key("a.b.c", data) is None
    # Missing root
    assert get_key("x.y", data) is None
