# derived from https://github.com/altair-viz/altair/blob/8a8642b2e7eeee3b914850a8f7aacd53335302d9/altair/utils/plugin_registry.py
from dataclasses import dataclass
from typing import TypeVar, Any, Generic, Dict, Union, List, cast
import sys
import functools

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

PluginType = TypeVar("PluginType")

@dataclass
class ActivePlugin(Generic[PluginType]):
    name: str
    plugin: PluginType
    options: Dict[str, Any]

class PluginEnabler(Generic[PluginType]):
    """Context manager for enabling plugins.

    This object lets you use enable() as a context manager to
    temporarily enable a given plugin::
        with plugins.enable('name'):
            do_something()  # 'name' plugin temporarily enabled
        # plugins back to original state
    """

    def __init__(
        self,
        registry: "PluginRegistry[PluginType]",
        reset: Union[None, ActivePlugin[PluginType]],
    ):
        self.registry = registry
        self.reset = reset

    def __enter__(self) -> "PluginEnabler[PluginType]":
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.registry._active = self.reset

    def __repr__(self) -> str:
        return "{}.enable({!r})".format(
            self.registry.__class__.__name__, self.registry.active
        )


class PluginRegistry(Generic[PluginType]):
    """A registry for plugins.

    This is a plugin registry that allows plugins to be loaded/registered
    in two ways:

    1. Through an explicit call to ``.register(name, value)``.
    2. By looking for other Python packages that are installed and provide
       a setuptools entry point group.
    When you create an instance of this class, provide the name of the
    entry point group to use::

        reg = PluginRegister('my_entrypoint_group')

    """

    def __init__(self, entry_point_group: str = ""):
        self.entry_point_group = entry_point_group
        self._active = None  # type: Union[None, ActivePlugin[PluginType]]
        self._plugins = {}  # type: Dict[str, PluginType]

    def register(
        self, name: str, value: Union[PluginType, None]
    ) -> Union[PluginType, None]:
        """Register a plugin by name and value.

        This method is used for explicit registration of a plugin and shouldn't be
        used to manage entry point managed plugins, which are auto-loaded.

        Parameters
        ==========
        name: str
            The name of the plugin.
        value: PluginType or None
            The actual plugin object to register or None to unregister that plugin.

        Returns
        =======
        plugin: PluginType or None
            The plugin that was registered or unregistered.
        """
        if value is None:
            return self._plugins.pop(name, None)
        else:
            self._plugins[name] = value
            return value

    def names(self) -> List[str]:
        """List the names of the registered and entry points plugins."""
        names = list(self._plugins.keys())
        names.extend(e.name for e in entry_points(group=self.entry_point_group))
        return sorted(set(names))

    def enable(self, name: Union[None, str] = None, **options) -> PluginEnabler:
        """Enable a plugin by name.

        This can be either called directly, or used as a context manager.
        Parameters
        ----------
        name : string (optional)
            The name of the plugin to enable. If not specified, then use the
            current active name.
        **options :
            Any additional parameters will be passed to the plugin as keyword
            arguments

        Returns
        -------
        PluginEnabler:
            An object that allows enable() to be used as a context manager
        """
        name = name or self.active

        if name not in self._plugins and (plugin := self._find_plugin(name)):
            self.register(name, plugin)

        prev = self._active
        self._active = ActivePlugin(name, self._plugins[name], options)
        return PluginEnabler(self, reset=prev)

    def _find_plugin(self, name: str) -> Union[PluginType, None]:
        """Find and load named EntryPoint.

        Raises if multiple EntryPoints have conflicting names.

        Parameters
        ==========
        name: str
            The name of the plugin.

        Returns
        =======
        plugin: PluginType or None
            The (un)found plugin
        """
        eps = entry_points(group=self.entry_point_group, name=name)
        if len(eps) == 0:
            return None
        assert len(eps) == 1, f"Conflicting entry-point '{name}'"
        return cast(PluginType, tuple(eps)[0].load())

    @property
    def active(self) -> str:
        """Return the name of the currently active plugin."""
        return "" if self._active is None else self._active.name

    @property
    def options(self) -> Dict[str, Any]:
        """Return the current options dictionary."""
        return {} if self._active is None else self._active.options

    def get(self) -> Union[None, PluginType]:
        """Return the currently active plugin."""
        if active := self._active:
            if active.options and callable(active.plugin):
                return functools.partial(active.plugin, **active.options)
            return active.plugin

    def __repr__(self) -> str:
        return "{}(active={!r}, registered={!r})" "".format(
            self.__class__.__name__, self.active, self.names()
        )
