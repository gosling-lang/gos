import { embed, GoslingComponent } from 'gosling.js/dist/src';
import type { GoslingSpec } from 'gosling.js/dist/src';

import React from 'react';
import ReactDOM  from 'react-dom';

// @ts-ignore
import css from '../node_modules/higlass/dist/hglib.css';
const style = document.createElement('style');
style.innerText = css;
document.head.appendChild(style).setAttribute('type', 'text/css');

export function render(selector: string, spec: GoslingSpec) {
	const el = document.getElementById(selector.substring(1))!;
	const ref = React.createRef<any>();
	return ReactDOM.render(
		<GoslingComponent ref={ref} spec={spec}/>,
		el,
		() => {
			let api: any;
			let interval = setInterval(() => {
				if (ref.current.api) {
					api = ref.current.api;
					api.exportPNG();
					clearInterval(interval);
				}
			}, 10000);
		}
	);
}

export { embed as gosingEmbed };

