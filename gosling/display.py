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
  <link rel="stylesheet" href="{{ higlass_css_url }}">
</head>
<body>
  <div id="{{ output_div }}"></div>
  <script type="module">

    async function loadScript(src) {
        return new Promise(resolve => {
            const script = document.createElement('script');
            script.onload = resolve;
            script.src = src;
            script.async = false;
            document.head.appendChild(script);
        });
    }

    async function loadGosling() {
        // Manually load scripts from window namespace since requirejs might not be
        // available in all browser environments.

        // https://github.com/DanielHreben/requirejs-toggle
        if (!window.gosling) {

            // https://github.com/DanielHreben/requirejs-toggle
            window.__requirejsToggleBackup = {
                define: window.define,
                require: window.require,
                requirejs: window.requirejs,
            };

            for (const field of Object.keys(window.__requirejsToggleBackup)) {
                window[field] = undefined;
            }

            // load dependencies sequentially
            const sources = [
                "{{ react_url }}",
                "{{ react_dom_url }}",
                "{{ pixijs_url }}",
                "{{ higlass_js_url }}",
                "{{ gosling_url }}",
            ];

            for (const src of sources) await loadScript(src);

            // restore requirejs after scripts have loaded
            Object.assign(window, window.__requirejsToggleBackup);
            delete window.__requirejsToggleBackup;

        }

        return window.gosling;
    };

    var el = document.getElementById('{{ output_div }}');
    var spec = {{ spec }};
    var opt = {{ embed_options }};

    loadGosling()
        .then(gosling => gosling.embed(el, spec, opt))
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
    higlass_version: str = "1.11",
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
