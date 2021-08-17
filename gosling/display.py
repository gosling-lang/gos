import json
import uuid

import jinja2

HTML_TEMPLATE = jinja2.Template(
    """
<!DOCTYPE html>
<html>
<head>
  <style>
    .error { color: red; }
  </style>
  <link rel="stylesheet" href="{{ base_url }}/higlass@{{ higlass_version }}/dist/hglib.css">
  <script type="text/javascript" src="{{ base_url }}/gosling.js@{{ gosling_version }}/dist/gosling.js"></script>
  <script type="text/javascript" src="{{ base_url }}/react@{{ react_version }}/umd/react.production.min.js"></script>
  <script type="text/javascript" src="{{ base_url }}/react-dom@{{ react_dom_version }}/umd/react-dom.production.min.js"></script>
  <script type="text/javascript" src="{{ base_url}}/pixi.js@{{ pixijs_version }}/dist/pixi.js"></script>
</head>
<body>
  <div id="{{ output_div }}"></div>
  <script>
    var spec = {{ spec }};
    var embedOpt = {{ embed_options }};
    var output_area = this;
    function showError(el, error) {
        el.innerHTML = ('<div class="error" style="color:red;">'
              + '<p>JavaScript Error: ' + error.message + '</p>'
              + "<p>This usually means there's a typo in your chart specification. "
              + "See the javascript console for the full traceback.</p>"
              + '</div>');
        throw error;
    }
    gosling.embed(document.getElementById('{{ output_div }}'), spec, embedOpt)
        .catch(error => showError(el, error));
  </script>
</body>
</html>
"""
)


def spec_to_html(
    spec,
    gosling_version,
    higlass_version,
    react_version,
    react_dom_version,
    pixijs_version,
    base_url="https://cdn.jsdelivr.net/npm/",
    output_div="vis",
    embed_options=None,
    json_kwds=None,
):
    embed_options = embed_options or {}
    json_kwds = json_kwds or {}

    return HTML_TEMPLATE.render(
        spec=json.dumps(spec, **json_kwds),
        embed_options=json.dumps(embed_options, **json_kwds),
        gosling_version=gosling_version,
        higlass_version=higlass_version,
        react_version=react_version,
        react_dom_version=react_dom_version,
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
        print(html)
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
