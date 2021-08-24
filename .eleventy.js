const fs = require('fs');
const { resolve } = require('path');
const { spawn } = require('child_process');

const hljs = require('highlight.js/lib/core');
hljs.registerLanguage('python', require('highlight.js/lib/languages/python'));

const renderSpec = (path) => {
  const proc = spawn('python', ['-m', 'gosling.utils.execeval', path]);
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
  config.addNunjucksAsyncShortcode('spec', ({ file }) => {
    const path = resolve(__dirname, 'example', file + '.py');
    return renderSpec(path);
  });

  config.addNunjucksAsyncShortcode('code', ({ file }) => {
    const path = resolve(__dirname, 'example', file + '.py');
    return readAndHighlight(path);
  });

  return {
    ...config,
    dir: {
      data: '',
      layouts: '',
      input: 'example/index.njk',
      output: 'dist',
    },
  };
};
