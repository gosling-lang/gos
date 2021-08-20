import { defineConfig } from "vite";
import fs from "fs";
import path from "path";
import url from "url";
import { spawn } from "child_process";

import chokidar from "chokidar";
import hljs from "highlight.js/lib/core";
import py from "highlight.js/lib/languages/python";

const language = "python";
hljs.registerLanguage(language, py);
const highlight = (python) => hljs.highlight(python, { language }).value;

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
const resolve = (fp) => path.resolve(__dirname, "examples", fp);

const renderSpec = (example) => {
  const proc = spawn("python", ["./examples/render.py", example]);
  return new Promise((resolve, reject) => {
    let buffer;
    proc.stdout.on("data", (buf) => {
      buffer = Buffer.concat(buffer ? [buffer, buf] : [buf]);
    });
    proc.stderr.on("data", (buf) => reject(buf.toString()));
    proc.on("close", () => resolve(buffer));
  });
};

const render = async (example) => {
  const [spec, python, template] = await Promise.all([
    renderSpec(example),
    fs.promises.readFile(example),
    fs.promises.readFile(resolve("index.html")),
  ]).then((bufs) => bufs.map((b) => b.toString()));

  const html = template
    .replace("<!--PYTHON_CODE-->", highlight(python))
    .replace("<!--SPEC-->", `<script>var SPEC = ${spec};</script>`);

  const htmlFp = example.split(".").slice(0, -1).join(".") + ".html";
  return fs.promises.writeFile(htmlFp, html);
};

const entries = {
  bar_chart: resolve("basic_marks/bar_chart.html"),
  line_chart: resolve("basic_marks/line_chart.html"),
  point_plot: resolve("basic_marks/point_plot.html"),
  ideograms: resolve("basic_marks/ideograms.html"),
  area_chart: resolve("basic_marks/area_chart.html"),
  text_marks: resolve("basic_marks/text_marks.html"),
  comparative_matrices: resolve("composite_vis/comparative_matrices.html"),
};

export default async ({ command }) => {
  const pythonFiles = Object
    .values(entries)
    .map((f) => f.split(".").slice(0, -1).join(".") + ".py");

  await Promise.all(pythonFiles.map(render));

  if (command === "serve") {
    const watcher = chokidar.watch(["./examples/index.html", ...pythonFiles]);
    watcher.on("change", (path) => {
      if (path.includes(".py")) render(path);
      if (path.includes(".html")) {
        // need to render all py files since template changed
        pythonFiles.map(render);
      }
    });
  }

  return defineConfig({
    root: "examples",
    build: {
      rollupOptions: {
        input: { index: resolve("index.html"), ...entries },
      },
    },
  });
};
