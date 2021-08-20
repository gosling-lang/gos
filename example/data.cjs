const fs = require('fs');
const { resolve } = require('path');
const { spawn } = require('child_process');

const hljs = require('highlight.js/lib/core');
hljs.registerLanguage('python', require('highlight.js/lib/languages/python'));

const render = (path) => {
  path = resolve(__dirname, path);
  const proc = spawn('python', ['./example/render.py', path]);
  return new Promise((resolve, reject) => {
    let buffer;
    proc.stdout.on('data', (buf) => {
      buffer = Buffer.concat(buffer ? [buffer, buf] : [buf]);
    });
    proc.stderr.on('data', (buf) => reject(buf.toString()));
    proc.on('close', () => resolve(buffer));
  });
};

const readAndHighlight = async (path) => {
  path = resolve(__dirname, path);
  const text = await fs.promises.readFile(path, { encoding: 'utf-8' });
  return hljs.highlight(text, { language: 'python' }).value;
};

module.exports = {
  routes: [
    { dir: 'basic_marks', name: 'bar_chart', title: 'Bar Chart' },
    { dir: 'basic_marks', name: 'line_chart', title: 'Line Chart' },
    { dir: 'basic_marks', name: 'point_plot', title: 'Point Plot' },
  ],
  eleventyComputed: {
    code: (data) => {
      const path = resolve(__dirname, data.dir, data.name + '.py');
      return readAndHighlight(path);
    },
    spec: (data) => {
      const path = resolve(__dirname, data.dir, data.name + '.py');
      return render(path);
    },
  },
};
