from gosling.plugin_registry import PluginRegistry
from typing import Callable


class TypedCallableRegistry(PluginRegistry[Callable[[int], int]]):
    ...


class GeneralCallableRegistry(PluginRegistry):
    ...


def test_plugin_registry():
    plugins = TypedCallableRegistry()

    assert plugins.names() == []
    assert plugins.active == ""
    assert plugins.get() is None
    assert repr(plugins) == "TypedCallableRegistry(active='', registered=[])"

    plugins.register("new_plugin", lambda x: x**2)
    assert plugins.names() == ["new_plugin"]
    assert plugins.active == ""
    assert plugins.get() is None
    assert repr(plugins) == (
        "TypedCallableRegistry(active='', " "registered=['new_plugin'])"
    )

    plugins.enable("new_plugin")
    assert plugins.names() == ["new_plugin"]
    assert plugins.active == "new_plugin"
    assert plugins.get()(3) == 9 # type: ignore
    assert repr(plugins) == (
        "TypedCallableRegistry(active='new_plugin', " "registered=['new_plugin'])"
    )


def test_plugin_registry_extra_options():
    plugins = GeneralCallableRegistry()

    plugins.register("metadata_plugin", lambda x, p=2: x**p)
    plugins.enable("metadata_plugin")
    assert plugins.get()(3) == 9 # type: ignore

    plugins.enable("metadata_plugin", p=3)
    assert plugins.active == "metadata_plugin"
    assert plugins.get()(3) == 27 # type: ignore

    # enabling without changing name
    plugins.enable(p=2)
    assert plugins.active == "metadata_plugin"
    assert plugins.get()(3) == 9 # type: ignore


def test_plugin_registry_context():
    plugins = GeneralCallableRegistry()

    plugins.register("default", lambda x, p=2: x**p)

    # At first there is no plugin enabled
    assert plugins.active == ""
    assert plugins.options == {}

    # Make sure the context is set and reset correctly
    with plugins.enable("default", p=6):
        assert plugins.active == "default"
        assert plugins.options == {"p": 6}

    assert plugins.active == ""
    assert plugins.options == {}

    # Make sure the context is reset even if there is an error
    try:
        with plugins.enable("default", p=6):
            assert plugins.active == "default"
            assert plugins.options == {"p": 6}
            raise ValueError()
    except ValueError:
        pass

    assert plugins.active == ""
    assert plugins.options == {}

    # Enabling without specifying name uses current name
    plugins.enable("default", p=2)

    with plugins.enable(p=6):
        assert plugins.active == "default"
        assert plugins.options == {"p": 6}

    assert plugins.active == "default"
    assert plugins.options == {"p": 2}
