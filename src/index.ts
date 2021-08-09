import { embed } from 'gosling.js';
import type { GoslingSpec } from 'gosling.js';

// @ts-ignore
import css from 'higlass/dist/hglib.css';
declare const css: string;

const style = document.createElement('style');
style.innerText = css;
document.head.appendChild(style).setAttribute('type', 'text/css');

type EmbedOptions = Parameters<typeof embed>[2];

export function render(selector: string, spec: GoslingSpec, opts?: EmbedOptions) {
	const el = document.getElementById(selector.substring(1))!;
	embed(el, spec, opts);
}

export { embed as goslingEmbed };
