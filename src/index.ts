import { embed } from 'gosling.js/dist/src';
import type { GoslingSpec } from 'gosling.js/dist/src';

//@ts-ignore
import css from 'higlass/dist/hglib.css';
const style = document.createElement('style');
style.innerText = css;
document.head.appendChild(style).setAttribute('type', 'text/css');

type EmbedOptions = Parameters<typeof embed>[2];

export function render(selector: string, spec: GoslingSpec, options: EmbedOptions = {}) {
	const el = document.getElementById(selector.substring(1))!;
	embed(el, spec, options);
}

export { embed as goslingEmbed };
