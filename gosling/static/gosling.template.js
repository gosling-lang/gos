const spec = {spec};
const opt = {opt};
const id = "{id}";

require(["nbextensions/jupyter-gosling/index"], function(gos) {{
	const target = document.createElement("div");
	target.id = id;
	target.className = "gosling-embed";

	// element is a jQuery wrapped DOM element inside the output area
	// see http://ipython.readthedocs.io/en/stable/api/generated/\
	// IPython.display.html#IPython.display.Javascript.__init__
	element[0].appendChild(target);
	gos.render("#" + id, spec, opt);
}}, (err) => {{
	if (err.requireType !== "scripterror") throw(err);
}});
