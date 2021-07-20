import { embed, GoslingSpec } from 'gosling.js/dist/src';

type EmbedOptions = Parameters<typeof embed>[2];

export function render(selector: string, spec: GoslingSpec, options: EmbedOptions = {}) {
  // Never been rendered, so render JS and append the PNG to the
  // outputs for the cell
  const el = document.getElementById(selector.substring(1))!;
  embed(el, spec, options);
}

export { embed  as goslingEmbed };
