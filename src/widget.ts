import { DOMWidgetView } from "@jupyter-widgets/base";
import { goslingEmbed } from "./index";

type EmbedParameters = Parameters<typeof goslingEmbed>;
type GoslingSpec = EmbedParameters[1];
type EmbedOptions = EmbedParameters[2];

export class GoslingWidget extends DOMWidgetView {
  viewElement = document.createElement("div");
  errorElement = document.createElement("div");

  async render() {
    this.el.appendChild(this.viewElement);
    this.errorElement.style.color = "red";
    this.el.appendChild(this.errorElement);

    const reembed = async () => {
      const spec: GoslingSpec = JSON.parse(this.model.get("_spec_source"));
      const opt: EmbedOptions = JSON.parse(this.model.get("_opt_source")) || {};
      if (spec == null) {
        return;
      }
      try {
        goslingEmbed(this.viewElement, spec, opt);
        this.send({ type: "display" });
      } catch (err) {
        console.error(err);
      }
    };

    this.model.on("change:_spec_source", reembed);
    this.model.on("change:_opt_source", reembed);

    // initial rendering
    await reembed();
  }
}
