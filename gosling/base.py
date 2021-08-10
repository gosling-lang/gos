import json
import pathlib
import uuid
from typing import Optional, TypedDict, Union

from IPython.display import display

from gosling.schema import Root

JS_TEMPLATE = pathlib.Path(__file__).parent / "static" / "gosling.template.js"

Options = TypedDict(
    "Options",
    {
        "padding": Optional[float],
        "margin": Optional[Union[str, float]],
        "border": Optional[str],
        "id": Optional[str],
        "className": Optional[str],
        # TODO: "theme":
    },
)


class Gosling:
    def __init__(self, spec: Union[dict, Root], opt: Optional[Options] = None):
        self.spec = spec if not isinstance(spec, Root) else spec.to_dict()
        self.opt = opt or {}

    def _generate_js(self, id, **kwrgs):
        with open(JS_TEMPLATE, encoding="utf-8") as f:
            template = f.read()
        payload = template.format(
            id=id,
            spec=json.dumps(self.spec, **kwrgs),
            opt=json.dumps(self.opt, **kwrgs),
        )
        return payload

    def _repr_mimebundle_(self, include=None, exclude=None):
        """Display the visualization in the Jupyter notebook."""
        id = uuid.uuid4()
        return (
            {"application/javascript": self._generate_js(id)},
            {"jupyter-gosling": "#{0}".format(id)},
        )

    def display(self):
        """Render the visualization."""
        display(self)
