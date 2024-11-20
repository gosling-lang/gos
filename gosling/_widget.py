import json
import pathlib
from typing import Any, Dict
import warnings

import anywidget
import traitlets as t

try:
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
except FileNotFoundError:
    warnings.warn("GoslingWidget: ESM not found. Must build frontend assets.")
    _esm = None


class GoslingWidget(anywidget.AnyWidget):
    _esm = _esm
    _viewconf = t.Unicode("null").tag(sync=True)

    location = t.List(t.Union([t.Float(), t.Tuple()]), read_only=True).tag(sync=True)

    def __init__(self, viewconf: Dict[str, Any], **kwargs):
        super().__init__(_viewconf=json.dumps(viewconf), **kwargs)

    def zoom_to(self, view_id: str, pos: str, padding: float = 0, duration: int = 1000):
        msg = json.dumps(["zoomTo", view_id, pos, padding, duration])
        self.send(msg)
