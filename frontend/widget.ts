import * as gosling from "gosling.js";

interface Model {
  _viewconf: string;
}

export default {
  async render({ model, el }: import("@anywidget/types").RenderProps<Model>) {
    const viewconf = JSON.parse(model.get("_viewconf"));
    const api = await gosling.embed(el, viewconf, { padding: 0 });
    model.on("msg:custom", (msg) => {
      msg = JSON.parse(msg);
      console.log(msg);
      try {
        const [fn, ...args] = msg;
        // @ts-expect-error - This is a dynamic call
        api[fn](...args);
      } catch (e) {
        console.error(e);
      }
    });
  },
};
