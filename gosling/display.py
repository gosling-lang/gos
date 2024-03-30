from __future__ import annotations

import json
import uuid
from typing import Any, Dict

import jinja2

from gosling.plugin_registry import PluginRegistry
from gosling.schema import SCHEMA_VERSION, THEMES

# TODO: Ideally we could use a single import but this seems to work ok.
HTML_TEMPLATE = jinja2.Template(
    """
<!DOCTYPE html>
<html>
<head>
  <style>.error { color: red; }</style>
</head>
<body>
  <div id="{{ output_div }}"></div>
  <script type="module">
    import { importWithMap } from "https://unpkg.com/dynamic-importmap@0.1.0";
    let importMap = {{ import_map }};
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


def get_gosling_import_map(
    gosling_version: str = SCHEMA_VERSION.lstrip("v"),
    higlass_version: str = "1.13",
    react_version: str = "18",
    pixijs_version: str = "6",
) -> dict:
    return {
        "imports": {
            "react": f"https://esm.sh/react@{react_version}",
            "react-dom": f"https://esm.sh/react-dom@{react_version}",
            "pixi": f"https://esm.sh/pixi.js@{pixijs_version}",
            "higlass": f"https://esm.sh/higlass@{higlass_version}?external=react,react-dom,pixi",
            "gosling.js": f"https://esm.sh/gosling.js@{gosling_version}?external=react,react-dom,pixi,higlass",
        }
    }


def spec_to_html(
    spec: GoslingSpec,
    output_div: str = "vis",
    embed_options: Dict[str, Any] | None = None,
    **kwargs,
):
    embed_options = embed_options or dict(padding=0, theme=themes.get())
    deps = get_gosling_import_map(**kwargs)

    return HTML_TEMPLATE.render(
        spec=json.dumps(spec),
        embed_options=json.dumps(embed_options),
        output_div=output_div,
        import_map=json.dumps(deps),
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
