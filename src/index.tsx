import React from 'react';
import ReactDOM from 'react-dom';

import { GoslingComponent as _GoslingComponent } from 'gosling.js/dist/src';
import html2canvas from 'html2canvas';
import type { GoslingSpec, Theme } from 'gosling.js/dist/src';

type EmbedOptions = {
	padding?: number;
	margin?: number | string;
	border?: string;
	id?: string;
	className?: string;
	theme?: Theme;
}

function GoslingComponent(props: {
	spec: GoslingSpec,
	options?: EmbedOptions,
	onRender?: () => void,
}) {
	React.useEffect(() => { props.onRender?.() }, []);
	return <_GoslingComponent
		spec={props.spec}
		padding={props.options?.padding}
		margin={props.options?.margin}
		border={props.options?.border}
		id={props.options?.id}
		className={props.options?.className}
		theme={props.options?.theme}
	/>;
}

function embed(el: HTMLElement, spec: GoslingSpec, options?: EmbedOptions) {
	return new Promise<void>((resolve, reject) => {
		try {
			ReactDOM.render(
				<GoslingComponent spec={spec} options={options} onRender={resolve}/>,
				el,
			);
		} catch (err) {
			reject(err);
		}
	});
}


//@ts-ignore
import css from './hglib@1.11.3.css';
const style = document.createElement('style');
style.innerText = css;
document.head.appendChild(style).setAttribute('type', 'text/css');


function javascriptIndex(selector: string, outputs: any) {
	// Return the index in the output array of the JS repr of this viz
	for (let i = 0; i < outputs.length; i++) {
	  const item = outputs[i];
	  if (
		item.metadata &&
		item.metadata["jupyter-gosling"] === selector &&
		item.data["application/javascript"] !== undefined
	  ) {
		return i;
	  }
	}
	return -1;
  }
  
  function imageIndex(selector: string, outputs: any) {
	// Return the index in the output array of the PNG repr of this viz
	for (let i = 0; i < outputs.length; i++) {
	  const item = outputs[i];
	  if (
		item.metadata &&
		item.metadata["jupyter-gosling"] === selector &&
		item.data["image/png"] !== undefined
	  ) {
		return i;
	  }
	}
	return -1;
  }
  
  function showError(el: HTMLElement, error: Error) {
	el.innerHTML = `<div class="error">
	  <p>Javascript Error: ${error.message}</p>
	  <p>This usually means there's a typo in your chart specification.
	  See the JavaScript console for the full traceback.</p>
	</div>`;
  
	throw error;
  }

export function render(selector: string, spec: GoslingSpec, options: EmbedOptions = {}, output_area: any) {
	// Find the indices of this visualizations JS and PNG
	// representation.
	const imgIndex = imageIndex(selector, output_area.outputs);
	const jsIndex = javascriptIndex(selector, output_area.outputs);

	// If we have already rendered a static image, don't render
	// the JS version or append a new PNG version
	if (imgIndex > -1 && jsIndex > -1) {
		return;
	}

	const el = document.getElementById(selector.substring(1))!;
	embed(el, spec, options)
		.then(() => html2canvas(el))
		.then(canvas => canvas.toDataURL("image/png"))
		.then(imageData => {
			if (output_area !== undefined) {
				const output = {
					data: { "image/png": imageData.split(",")[1] },
					metadata: { "jupyter-gosling": selector },
					output_type: "display_data",
				};
				// This appends the PNG output, but doesn't render it this time
				// as the JS version will be rendered already.
				output_area.outputs.push(output);
			  }
		})
		.catch(err => { showError(el, err); });
}

export { embed as goslingEmbed };
