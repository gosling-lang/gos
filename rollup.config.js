import alias from '@rollup/plugin-alias';
import commonjs from '@rollup/plugin-commonjs';
import json from '@rollup/plugin-json';
import resolve from '@rollup/plugin-node-resolve';
import esbuild from 'rollup-plugin-esbuild';

const name = 'nbextension/gosling/index';

const plugins = () => [
    alias({ entries: {"gosling.js/dist/src": "gosling.js"}}),
    resolve({ browser: true }),
    commonjs(),
    json(),
    esbuild(),
];

/** @type {import('rollup').RollupOptions[]}*/
const config = [
    {
        input: 'src/index.ts',
        output: {
            file: 'gosling/static/index.js',
            format: 'amd',
            name: name,
        },
        plugins: plugins(),
    },
    {
        input: 'src/widget.ts', 
        output: {
            file: 'gosling/static/widget.js',
            format: 'amd',
        },
        external: ['@jupyter-widgets/base', name],
        plugins: [
            alias({ entries: { './index': name } }),
            ...plugins(),
        ],
    }
];

export default config;
