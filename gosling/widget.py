import json
from typing import Optional, TypedDict, Union

from gosling.schema import Root

try:
    from ipywidgets import DOMWidget
    from traitlets import Unicode

except ImportError as err:
    raise ImportError(
        "gosling.widget requires ipywidgets, which could not be imported. "
        "Is ipywidgets installed?"
    )

__all__ = ["GoslingWidget"]

EmbedOptions = TypedDict(
    "EmbedOptions",
    {
        "padding": Optional[float],
        "margin": Optional[Union[str, float]],
        "border": Optional[str],
        "id": Optional[str],
        "className": Optional[str],
        # TODO: "theme":
    },
)


class GoslingWidget(DOMWidget):
    _view_module = Unicode("nbextensions/jupyter-gosling/widget").tag(sync=True)
    _view_module_version = Unicode("0.0.0").tag(sync=True)
    _view_name = Unicode("GoslingWidget").tag(sync=True)

    _spec_source = Unicode("null").tag(sync=True)
    _opt_source = Unicode("null").tag(sync=True)

    def __init__(
        self, spec: Optional[Root] = None, opt: Optional[EmbedOptions] = None, **kwargs
    ):
        super().__init__(**kwargs)
        self._spec_source = spec.to_json()
        self._opt_source = json.dumps(opt)

    @property
    def spec(self):
        return Root.from_dict(self._spec_source)

    @spec.setter
    def spec(self, value: Root):
        self._spec_source = value.to_json()

    @property
    def opt(self):
        return json.loads(self._opt_source)

    @opt.setter
    def opt(self, value: EmbedOptions):
        self._opt_source = json.dumps(value)
        self._reset()
