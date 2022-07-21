import json
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Set, Union

import jinja2

from gosling.schema import SCHEMA_VERSION, THEMES

HTML_TEMPLATE = jinja2.Template(
    """
<!DOCTYPE html>
<html>
<head>
  <style>.error { color: red; }</style>
  <link rel="stylesheet" href="{{ css_url }}">
</head>
<body>
  <div id="{{ output_div }}"></div>
  <script type="module">
    import * as gosling from '{{ js_url }}';
    var el = document.getElementById('{{ output_div }}');
    var spec = {{ spec }};
    var opt = {{ embed_options }};
    gosling.embed(el, spec, opt)
        .catch(err => {
            el.innerHTML = `\
<div class="error">
    <p>JavaScript Error: ${error.message}</p>
    <p>This usually means there's a typo in your Gosling specification. See the javascript console for the full traceback.</p>
</div>`;
            throw error;
        });
  </script>
</body>
</html>
"""
)

GoslingSpec = Dict[str, Any]

def get_vis_dependencies(
    gosling_version: str = SCHEMA_VERSION.lstrip("v"),
    higlass_version: str = "1.11",
    react_version: str = "17",
    pixijs_version: str = "6",
):
    js_url = f"https://esm.sh/gosling.js@{gosling_version}?bundle&target=2018&deps="
    js_url += f"higlass@{higlass_version},"
    js_url += f"react@{react_version},"
    js_url += f"react-dom@{react_version},"
    js_url += f"pixi.js@{pixijs_version}"
    css_url = f"https://esm.sh/higlass@{higlass_version}/dist/hglib.css"
    return js_url, css_url


def spec_to_html(
    spec: GoslingSpec,
    output_div: str = "vis",
    embed_options: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    js_url, css_url = get_vis_dependencies(**kwargs)
    embed_options = embed_options or dict(padding=0, theme=themes.get())

    return HTML_TEMPLATE.render(
        spec=json.dumps(spec),
        embed_options=json.dumps(embed_options),
        output_div=output_div,
        js_url=js_url,
        css_url=css_url,
    )


class Renderer:
    def __init__(self, output_div: str = "jupyter-gosling-{}", **kwargs: Any):
        self._output_div = output_div
        self.kwargs = kwargs

    @property
    def output_div(self) -> str:
        return self._output_div.format(uuid.uuid4().hex)

    def __call__(self, spec: GoslingSpec, **meta: Any) -> Dict[str, Any]:
        raise NotImplementedError()


class HTMLRenderer(Renderer):
    def __call__(self, spec: GoslingSpec, **meta: Any):
        kwargs = self.kwargs.copy()
        kwargs.update(meta)
        html = spec_to_html(spec=spec, output_div=self.output_div, **kwargs)
        return {"text/html": html}


html_renderer = HTMLRenderer()

CustomTheme = Dict[str, Any]


@dataclass
class ThemesRegistry:
    themes: Set[str]
    custom_themes: Dict[str, CustomTheme] = field(default_factory=dict)
    active: Optional[str] = None

    def register(self, name: str, theme: CustomTheme) -> None:
        assert (
            name not in self.themes
        ), f"cannot override built-in themes, {self.themes}"
        self.custom_themes[name] = theme

    def enable(self, name: str) -> None:
        assert (
            name in self.custom_themes or name in self.themes
        ), f"theme must be one of {self.themes} or {set(self.custom_themes.keys())}."
        self.active = name

    def get(self) -> Union[None, str, CustomTheme]:
        if self.active is None:
            return None
        if self.active in self.themes:
            return self.active
        return self.custom_themes[self.active]


themes = ThemesRegistry(THEMES)
