import json
import uuid
from dataclasses import dataclass
from typing import Optional, Union, TypedDict
import pathlib

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


@dataclass
class Gosling:
    spec: Root
    opt: Optional[Options] = None

    def _generate_js(self, id):
        with open(JS_TEMPLATE, encoding='utf-8') as f:
            template = f.read()
        payload = template.format(
            id=id,
            spec=self.spec.to_json(),
            opt=json.dumps(self.opt),
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
