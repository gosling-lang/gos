import json
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional

import jinja2

from gosling.plugin_registry import PluginRegistry
from gosling.schema import SCHEMA_VERSION, THEMES

# TODO: This is kind of a mess. Gosling.js can be very finky with its 
# peer dependencies in various Jupyter-like environments. This is a 
# hacky way to get things working in JupyterLab, Jupyter Notebook, 
# VSCode, and Colab consistently.
HTML_TEMPLATE = jinja2.Template(
    """
<!DOCTYPE html>
<html>
<head>
  <style>.error { color: red; }</style>
  <link rel="stylesheet" href="{{ higlass_css_url }}">
</head>
<body>
  <div id="{{ output_div }}"></div>
  <script type="module">
    import { importWithMap } from "https://unpkg.com/dynamic-importmap@0.1.0";
    let importMap = {
      imports: {
        "react": "https://esm.sh/react@18",
        "react-dom": "https://esm.sh/react-dom@18",
        "pixi": "https://esm.sh/pixi.js@6",
        "higlass": "https://esm.sh/higlass@1.13?external=react,react-dom,pixi",
        "gosling.js":
          "https://esm.sh/gosling.js@0.11.0?external=react,react-dom,pixi,higlass",
      },
    };
    let gosling = await importWithMap("gosling.js", importMap);
    let el = document.getElementById('{{ output_div }}');
    let spec = {{ spec }};
    let opt = {{ embed_options }};
    gosling.embed(el, spec, opt).catch((err) => {
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


@dataclass
class GoslingBundle:
    react: str
    react_dom: str
    pixijs: str
    higlass_js: str
    higlass_css: str
    gosling: str


def get_display_dependencies(
    gosling_version: str = SCHEMA_VERSION.lstrip("v"),
    higlass_version: str = "~1.12",
    react_version: str = "17",
    pixijs_version: str = "6",
    base_url: str = "https://unpkg.com",
) -> GoslingBundle:
    return GoslingBundle(
        react=f"{ base_url }/react@{ react_version }/umd/react.production.min.js",
        react_dom=f"{ base_url }/react-dom@{ react_version }/umd/react-dom.production.min.js",
        pixijs=f"{ base_url }/pixi.js@{ pixijs_version }/dist/browser/pixi.min.js",
        higlass_js=f"{ base_url }/higlass@{ higlass_version }/dist/hglib.js",
        higlass_css=f"{ base_url }/higlass@{ higlass_version }/dist/hglib.css",
        gosling=f"{ base_url }/gosling.js@{ gosling_version }/dist/gosling.js",
    )


def spec_to_html(
    spec: GoslingSpec,
    output_div: str = "vis",
    embed_options: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    embed_options = embed_options or dict(padding=0, theme=themes.get())
    deps = get_display_dependencies(**kwargs)

    return HTML_TEMPLATE.render(
        spec=json.dumps(spec),
        embed_options=json.dumps(embed_options),
        output_div=output_div,
        react_url=deps.react,
        react_dom_url=deps.react_dom,
        pixijs_url=deps.pixijs,
        higlass_js_url=deps.higlass_js,
        higlass_css_url=deps.higlass_css,
        gosling_url=deps.gosling,
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


renderers = PluginRegistry[Renderer]("gosling.renderer")
renderers.register("default", HTMLRenderer())
renderers.enable("default")

CustomTheme = Dict[str, Any]

themes = PluginRegistry[CustomTheme]("gosling.theme")
for theme in THEMES:
    # Add builtin string themes
    themes.register(theme, theme)  # type: ignore
