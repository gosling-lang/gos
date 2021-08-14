import { embed, GoslingSpec } from 'gosling.js';

/**
 * Inject Higlass CSS. Esbuild is configured to inline the .css as text.
 */
// @ts-ignore
import css from 'higlass/dist/hglib.css';
declare const css: string;
const style = document.createElement('style');
style.innerText = css;
document.head.appendChild(style).setAttribute('type', 'text/css');

/**
 * Utils from https://github.com/vega/ipyvega/blob/master/src/index.ts
 */
type JupyterOutput = {
	metadata?: Record<string, unknown>;
	data: Record<string, unknown>;
	output_type: string;
};

function javascriptIndex(selector: string, outputs: JupyterOutput[]) {
	// Return the index in the output array of the JS repr of this viz
	for (let i = 0; i < outputs.length; i++) {
		const item = outputs[i];
		if (
			item.metadata &&
			item.metadata['jupyter-gosling'] === selector &&
			item.data['application/javascript'] !== undefined
		) {
			return i;
		}
	}
	return -1;
}

function imageIndex(selector: string, outputs: JupyterOutput[]) {
	// Return the index in the output array of the PNG repr of this viz
	for (let i = 0; i < outputs.length; i++) {
		const item = outputs[i];
		if (
			item.metadata &&
			item.metadata['jupyter-gosling'] === selector &&
			item.data['image/png'] !== undefined
		) {
			return i;
		}
	}
	return -1;
}

function showError(el: HTMLElement, error: Error) {
	el.innerHTML = `\
<div style="color:firebrick;font-size:14px">
	<p>Javascript Error: ${error.message}</p>
	<p>This usually means there's a typo in your chart specification. See the JavaScript console for the full traceback.</p>
</div>`;
	throw error;
}

const wait = (ms: number) => new Promise<void>((res) => setTimeout(res, ms));

export function render(
	selector: string,
	spec: GoslingSpec,
	opts?: Parameters<typeof embed>[2],
	output_area?: { outputs: JupyterOutput[] }
): void {

	// Find the indices of this visualizations JS and PNG representation.
	if (output_area) {
		const imgIndex = imageIndex(selector, output_area.outputs);
		const jsIndex = javascriptIndex(selector, output_area.outputs);
		// If we have already rendered a static image, don't render
		// the JS version or append a new PNG version
		if (imgIndex > -1 && jsIndex > -1) {
			return;
		}
	}

	const root = document.getElementById(selector.substring(1))!;
	embed(root, spec, opts)
		.then(async api => {
			if (!output_area) return;

			// TODO: any way to wait for full canvas render?
			await wait(200);

			const { canvas } = api.getCanvas({ resolution: 1 });
			const type = 'image/png';
			const output: JupyterOutput = {
				data: { [type]: canvas.toDataURL(type).split(',')[1] },
				metadata: { 'jupyter-gosling': selector },
				output_type: 'display_data',
			};
			output_area.outputs.push(output);
		})
		.catch(err => showError(root, err));
}

export { embed as goslingEmbed };
