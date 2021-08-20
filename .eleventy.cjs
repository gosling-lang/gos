const fs = require('fs');
const { resolve } = require('path');
const { spawn } = require('child_process');

const hljs = require('highlight.js/lib/core');
hljs.registerLanguage('python', require('highlight.js/lib/languages/python'));

const renderSpec = (path) => {
  const proc = spawn('python', ['./example/render.py', path]);
  return new Promise((resolve, reject) => {
    let buffer;
    proc.stdout.on('data', (buf) => {
      buffer = Buffer.concat(buffer ? [buffer, buf] : [buf]);
    });
    proc.stderr.on('data', (buf) => reject(buf.toString()));
    proc.on('close', () => resolve(buffer.toString()));
  });
};

const readAndHighlight = async (path) => {
  const text = await fs.promises.readFile(path, { encoding: 'utf-8' });
  return hljs.highlight(text, { language: 'python' }).value;
};

module.exports = (config) => {
  config.addNunjucksAsyncShortcode('spec', ({ dir, name }) => {
    const path = resolve(__dirname, 'example', dir, name + '.py');
    return renderSpec(path);
  });

  config.addNunjucksAsyncShortcode('code', ({ dir, name }) => {
    const path = resolve(__dirname, 'example', dir, name + '.py');
    return readAndHighlight(path);
  });

  return {
    ...config,
    dir: {
      data: '',
      layouts: '',
      input: 'example/example.njk',
      output: 'dist',
    },
  };
};
