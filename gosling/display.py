from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, TypeVar
from gosling.schema import SCHEMA_VERSION
import json
import uuid

import jinja2

HTML_TEMPLATE = jinja2.Template(
    """
<!DOCTYPE html>
<html>
<head>
  <style>.error { color: red; }</style>
  <link rel="stylesheet" href="{{ base_url }}/higlass@{{ higlass_version }}/dist/hglib.css">
</head>
<body>
  <div id="{{ output_div }}"></div>
  <script>
    function embed(gos) {
        var el = document.getElementById('{{ output_div }}');
        var spec = {{ spec }};
        var opt = {{ embed_options }};

        gos.embed(el, spec, opt).catch(err => {
            el.innerHTML = `\
<div class="error">
    <p>JavaScript Error: ${error.message}</p>
    <p>This usually means there's a typo in your chart specification. See the javascript console for the full traceback.</p>
</div>`;
            throw error;
        });
    }

    if (!window.gosling) {

        // Manually load scripts from window namespace since requirejs might not be
        // available in all browser environments.
        // https://github.com/DanielHreben/requirejs-toggle

        window.__requirejsToggleBackup = { define: window.define, require: window.require, requirejs: window.requirejs };
        for (const field of Object.keys(window.__requirejsToggleBackup)) {
            window[field] = undefined;
        }

        // load dependencies sequentially
        [
          "{{ base_url }}/react@{{ react_version }}/umd/react.production.min.js",
          "{{ base_url }}/react-dom@{{ react_version }}/umd/react-dom.production.min.js",
          "{{ base_url }}/pixi.js@{{ pixijs_version }}/dist/browser/pixi.min.js",
        ].forEach(src => {
            var script = document.createElement('script');
            script.src = src;
            script.async = false;
            document.head.appendChild(script);
        });

        // wait for gosling to load before restoring requirejs
        var script = document.createElement('script');
        script.onload = () => {
            // restore requirejs after scripts have loaded
            Object.assign(window, window.__requirejsToggleBackup);
            delete window.__requirejsToggleBackup;

            embed(window.gosling);
        }
        script.src = "{{ base_url }}/gosling.js@{{ gosling_version }}/dist/gosling.js",
        script.async = false;
        document.head.appendChild(script);

    } else {

        embed(window.gosling);
    }
  </script>
</body>
</html>
"""
)


def spec_to_html(
    spec,
    gosling_version=SCHEMA_VERSION.lstrip("v"),
    higlass_version="1.11",
    react_version="17",
    pixijs_version="6",
    base_url="https://unpkg.com",
    output_div="vis",
    embed_options=None,
    json_kwds=None,
):
    embed_options = embed_options or dict(padding=0)
    json_kwds = json_kwds or {}

    return HTML_TEMPLATE.render(
        spec=json.dumps(spec, **json_kwds),
        embed_options=json.dumps(embed_options, **json_kwds),
        gosling_version=gosling_version,
        higlass_version=higlass_version,
        react_version=react_version,
        pixijs_version=pixijs_version,
        base_url=base_url,
        output_div=output_div,
    )


JS_TEMPLATE = jinja2.Template(
    """
const spec = {{ spec }};
const opt = {{ embed_options }};
const id = "{{ output_div }}";

const output_area = this;

require(["nbextensions/jupyter-gosling/index"], function(gos) {
  const target = document.createElement("div");
  target.id = id;
  target.className = "gosling-embed";

  // element is a jQuery wrapped DOM element inside the output area
  // see http://ipython.readthedocs.io/en/stable/api/generated/\
  // IPython.display.html#IPython.display.Javascript.__init__
  element[0].appendChild(target);

  gos.render("#" + id, spec, opt, output_area);
}, (err) => {
    if (err.requireType !== "scripterror") throw(err);
});
"""
)


def spec_to_js(spec, output_div, embed_options=None, json_kwds=None):
    embed_options = embed_options or {}
    json_kwds = json_kwds or {}
    return JS_TEMPLATE.render(
        output_div=output_div,
        spec=json.dumps(spec, **json_kwds),
        embed_options=json.dumps(embed_options, **json_kwds),
    )


class BaseRenderer:
    def __init__(self, output_div="jupyter-gosling-{}", **kwargs):
        self._output_div = output_div
        self.kwargs = kwargs

    @property
    def output_div(self):
        return self._output_div.format(uuid.uuid4().hex)

    def __call__(self, spec, **metadata):
        raise NotImplementedError()


class HTMLRenderer(BaseRenderer):
    def __call__(self, spec, **metadata):
        kwargs = self.kwargs.copy()
        kwargs.update(metadata)
        html = spec_to_html(spec=spec, output_div=self.output_div, **kwargs)
        return {"text/html": html}


class JSRenderer(BaseRenderer):
    def __call__(self, spec, **metadata):
        kwargs = self.kwargs.copy()
        kwargs.update(metadata)
        output_div = self.output_div
        js = spec_to_js(spec=spec, output_div=output_div, **kwargs)
        return (
            {"application/javascript": js},
            {"jupyter-gosling": f"#{output_div}"},
        )


@dataclass
class RendererRegistry:
    renderers: Dict[str, Callable] = field(default_factory=dict)
    active: Optional[str] = None

    def register(self, name: str, fn: Callable):
        self.renderers[name] = fn

    def enable(self, name: str):
        assert name in self.renderers
        self.active = name

    def get(self):
        assert isinstance(self.active, str) and self.active in self.renderers
        return self.renderers[self.active]


html_renderer = HTMLRenderer()
js_renderer = JSRenderer()

renderers = RendererRegistry()
renderers.register("default", html_renderer)
renderers.register("html", html_renderer)
renderers.register("colab", html_renderer)
renderers.register("kaggle", html_renderer)
renderers.register("zeppelin", html_renderer)
renderers.register("js", js_renderer)
renderers.enable("default")
