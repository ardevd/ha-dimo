from custom_components.dimo.helpers import get_key


def test_simple_key():
    data = {"a": 1, "b": "foo"}
    assert get_key("a", data) == 1
    assert get_key("b", data) == "foo"


def test_nested_keys():
    data = {"a": {"b": {"c": 42}}}
    assert get_key("a.b.c", data) == 42


def test_missing_key_returns_default():
    data = {"a": 1}
    # Default is None
    assert get_key("a.b.c", data) is None
    # Custom default
    assert get_key("x.y", data, default="fallback") == "fallback"


def test_list_index_traversal():
    """Test traversing lists using integer indices."""
    data = {"vehicles": [{"id": "v1", "make": "Ford"}, {"id": "v2", "make": "Tesla"}]}

    # Access first item
    assert get_key("vehicles.0.make", data) == "Ford"
    # Access second item
    assert get_key("vehicles.1.make", data) == "Tesla"


def test_list_index_out_of_bounds():
    data = {"items": [1, 2, 3]}
    assert get_key("items.5", data) is None
    assert (
        get_key("items.-1", data) is None
    )  # We generally don't support negative indexing in string paths for safety


def test_invalid_list_index_type():
    data = {"items": [1, 2, 3]}
    # 'foo' is not an integer, so it cannot index the list
    assert get_key("items.foo", data) is None


def test_empty_path():
    assert get_key("", {"a": 1}) is None
    assert get_key("", {"a": 1}, default="default") == "default"
