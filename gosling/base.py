from typing import Union
from gosling.schema import Root
from gosling.display import JSRenderer  # , HTMLRenderer

GOSLING_VERSION = "0.9.1"
HIGLASS_VERSION = "1.11.3"
REACT_VERSION = "16"
REACT_DOM_VERSION = "16"
PIXIJS_VERSION = "5"

renderers = {
    # "html": HTMLRenderer(
    #     gosling_version=GOSLING_VERSION,
    #     higlass_version=HIGLASS_VERSION,
    #     react_version=REACT_VERSION,
    #     react_dom_version=REACT_DOM_VERSION,
    #     pixijs_version=PIXIJS_VERSION,
    # ),
    "js": JSRenderer(),
}


class Gosling:
    def __init__(self, spec: Union[dict, Root]):
        self.spec = spec

    def to_dict(self):
        return self.spec if isinstance(self.spec, dict) else self.spec.to_dict()

    def _repr_mimebundle_(self, include=None, exclude=None):
        dct = self.to_dict()
        renderer = renderers.get("js")
        return renderer(dct) if renderer else {}

    def display(self):
        from IPython.display import display

        display(self)
