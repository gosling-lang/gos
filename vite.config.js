import { defineConfig } from "vite";
import fs from "fs";
import path from "path";
import url from "url";
import { spawn } from "child_process";

import chokidar from "chokidar";

import hljs from "highlight.js/lib/core";
import py from "highlight.js/lib/languages/python";
hljs.registerLanguage("python", py);

const highlight = python => hljs.highlight(python, { language: 'python' }).value;
const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
const resolve = fp => path.resolve(__dirname, 'examples', fp);

const watcher = chokidar.watch([
  "./examples/basic_marks/*.py",
  "./examples/index.html",
]);

const renderSpec = (example) => {
  const proc = spawn("python", ["./examples/render.py", example]);
  return new Promise((resolve, reject) => {
    proc.stdout.on("data", resolve);
    proc.stderr.on("data", reject);
  });
};

const render = async (example) => {
  const [spec, python, template] = await Promise.all([
    renderSpec(example),
    fs.promises.readFile(example),
    fs.promises.readFile(resolve('index.html')),
  ]).then(bufs => bufs.map(b => b.toString()));

  const html = template
    .replace("<!--PYTHON_CODE-->", highlight(python))
    .replace("<!--SPEC-->", `<script>var SPEC = ${spec};</script>`);

  const htmlFp = example.split(".").slice(0, -1).join(".") + ".html";
  return fs.promises.writeFile(htmlFp, html);
};

watcher.on("add", async (path) => {
  if (path.includes(".py")) {
    render(path).catch((err) => console.warn(err));
  }
});

watcher.on("change", (path) => {
  if (path.includes(".py")) {
    render(path).catch((err) => console.warn(err));
  }
  if (path.includes(".html")) {
    // need to render all py files since template changed
    const files = watcher.getWatched();
    Object.entries(files).forEach(([dir, names]) => {
      names.forEach((name) => name.includes(".py") && render(`${dir}/${name}`));
    });
  }
});

export default defineConfig({
  root: "examples",
  build: {
	  rollupOptions: {
		  input: {
			  main: resolve(__dirname, 'index.html'),
			  nested: resolve(__dirname, 'nested/index.html')
		  }
	  }
  },
});
