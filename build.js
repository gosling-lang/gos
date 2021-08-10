import esbuild from 'esbuild';
import { resolve } from 'path';

const banner = (external) => {
	if (external.length === 0) {
		return 'define(["exports"], (exports) => {';
	}
	const mods = ['exports', ...external];
	return `\
define(${JSON.stringify(mods)}, (exports, ...__imports) => {
var __mods = Object.fromEntries(${JSON.stringify(mods.slice(1))}.map((n, i) => [n, i]));
var require = (name) => __imports[__mods[name]];
`;
};


const amd = ({ entry, outdir = 'gosling/static', external = [], plugins = [] }) => {
	return {
		entryPoints: [entry],
		outdir: outdir,
		bundle: true,
		format: 'cjs',
		minify: process.env.NODE_ENV === 'production',
		external: external,
		banner: { js: banner(external) },
		footer: { js: '\n});' },
		plugins: plugins,
		loader: {
			'.css': 'text',
		},
	};
};

const build = () => {
	const path = resolve('node_modules/gosling.js/dist/gosling.js');

	const configs = [
		{
			entry: 'src/index.ts',
			plugins: [
				{
					name: 'resolve-gosling',
					setup(build) {
						build.onResolve({ filter: /^gosling.js\/dist\/src$/ }, (_) => ({ path }));
					},
				},
			],
		},
		{
			entry: 'src/widget.ts',
			external: ['@jupyter-widgets/base', 'nbextensions/jupyter-gosling/index'],
		},
	].map(amd);

	configs.map(esbuild.build);
};

build();
