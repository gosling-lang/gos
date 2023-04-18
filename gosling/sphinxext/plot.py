import pathlib
import warnings

import jinja2
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import flag

from gosling.display import get_display_dependencies
from gosling.schemapi import SchemaValidationError
from gosling.utils.execeval import eval_block

TEMPLATE = jinja2.Template(
    """
<div id="{{ div_id }}">
<script>
  document.addEventListener("DOMContentLoaded", function(event) {
      var spec = {{ spec }};
      console.log(spec);
      var opt = { padding: 0 };
      var el = document.querySelector('#{{ div_id }}');
      gosling.embed(el, spec, opt).catch(console.err);
  });
</script>
</div>
"""
)


class gosling_plot(nodes.General, nodes.Element):
    pass


class GoslingPlotDirective(Directive):
    has_content = True

    option_spec = {"code-below": flag}

    def run(self):
        env = self.state.document.settings.env
        app = env.app

        show_code = True
        code_below = "code-below" in self.options

        code = "\n".join(self.content)

        if show_code:
            source_literal = nodes.literal_block(code, code)
            source_literal["language"] = "python"

        # get the name of the source file we are currently processing
        rst_source = pathlib.Path(self.state_machine.document["source"])
        rst_dir = rst_source.parent
        rst_filename = rst_source.name

        # use the source file name to construct a friendly target_id
        serialno = env.new_serialno("gosling-plot")
        rst_base = rst_filename.replace(".", "-")
        div_id = f"{rst_base}-gosling-plot-{serialno}"
        target_id = f"{rst_base}-gosling-source-{serialno}"
        target_node = nodes.target("", "", ids=[target_id])

        # create the node in which the plot will appear;
        # this will be processed by html_visit_gosling_plot
        plot_node = gosling_plot()
        plot_node["target_id"] = target_id
        plot_node["div_id"] = div_id
        plot_node["code"] = code
        plot_node["relpath"] = str(rst_dir / env.srcdir)
        plot_node["rst_source"] = rst_source
        plot_node["rst_lineno"] = self.lineno
        plot_node["output"] = "html"

        result = [target_node]

        if code_below:
            result += [plot_node]
        if show_code:
            result += [source_literal]
        if not code_below:
            result += [plot_node]

        return result


def html_visit_gosling_plot(self, node):
    # Execute the code, saving output and namespace
    try:
        chart = eval_block(node["code"])
    except Exception as e:
        warnings.warn(
            "gosling-plot: {}:{} Code Execution failed:"
            "{}: {}".format(
                node["rst_source"], node["rst_lineno"], e.__class__.__name__, str(e)
            )
        )
        raise nodes.SkipNode

    # Last line should be a chart; convert to spec dict
    try:
        spec = chart.to_json()
    except SchemaValidationError:
        raise ValueError("Invalid chart: {0}".format(node["code"]))

    # Pass relevant info into the template and append to the output
    html = TEMPLATE.render(div_id=node["div_id"], spec=spec)
    self.body.append(html)


def depart_gosling_plot(self, node):
    return


def builder_inited(app):
    app.add_css_file(app.config.higlass_css_url)
    app.add_js_file(app.config.react_url)
    app.add_js_file(app.config.reactdom_url)
    app.add_js_file(app.config.pixi_url)
    app.add_js_file(app.config.higlass_js_url)
    app.add_js_file(app.config.gosling_url)


def setup(app):
    deps = get_display_dependencies()
    app.add_config_value("react_url", deps.react, "html")
    app.add_config_value("reactdom_url", deps.react_dom, "html")
    app.add_config_value("pixi_url", deps.pixijs, "html")
    app.add_config_value("higlass_js_url", deps.higlass_js, "html")
    app.add_config_value("higlass_css_url", deps.higlass_css, "html")
    app.add_config_value("gosling_url", deps.gosling, "html")

    app.add_directive("gosling-plot", GoslingPlotDirective)
    app.add_node(gosling_plot, html=(html_visit_gosling_plot, depart_gosling_plot))

    app.connect("builder-inited", builder_inited)
    return {"version": "0.1"}
