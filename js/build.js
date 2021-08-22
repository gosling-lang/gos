const esbuild = require('esbuild');
const { resolve } = require('path');

/** @param {string[]} external */
const banner = (external = []) => {
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

const footer = '\n});';

/**
 * Support AMD output with esbuild: https://github.com/evanw/esbuild/issues/819
 * `banner(external) + cjsOutput + footer` === AMD module.
 *
 * @param {{ entry: string } & Omit<import('esbuild').BuildOptions, 'entryPoints' | 'bundle' | 'format' | 'banner' | 'footer'>} config
 * @returns {import('esbuild').BuildOptions}
 */
const amd = ({ entry, ...config }) => ({
	entryPoints: [entry],
	...config,
	bundle: true,
	format: 'cjs',
	banner: { js: banner(config.external) },
	footer: { js: footer },
});

const isProd = process.env.NODE_ENV === 'production';

const configs = [
	{
		entry: resolve(__dirname, 'src', 'index.ts'),
		outdir: resolve(__dirname, '..', 'gosling', 'static'),
		loader: { '.css': 'text' },
		minify: isProd,
		define: {
			'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
		},
	},
	{
		entry: resolve(__dirname, 'src', 'widget.ts'),
		outdir: resolve(__dirname, '..', 'gosling', 'static'),
		external: ['@jupyter-widgets/base', 'nbextensions/jupyter-gosling/index'],
		minify: isProd,
	},
];

configs.map(amd).map(esbuild.build);
