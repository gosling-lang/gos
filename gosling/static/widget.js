define(["exports","@jupyter-widgets/base","nbextensions/jupyter-gosling/index"], (exports, ...__imports) => {
var __mods = Object.fromEntries(["@jupyter-widgets/base","nbextensions/jupyter-gosling/index"].map((n, i) => [n, i]));
var require = (name) => __imports[__mods[name]];

var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __markAsModule = (target) => __defProp(target, "__esModule", { value: true });
var __export = (target, all) => {
  __markAsModule(target);
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __reExport = (target, module2, desc) => {
  if (module2 && typeof module2 === "object" || typeof module2 === "function") {
    for (let key of __getOwnPropNames(module2))
      if (!__hasOwnProp.call(target, key) && key !== "default")
        __defProp(target, key, { get: () => module2[key], enumerable: !(desc = __getOwnPropDesc(module2, key)) || desc.enumerable });
  }
  return target;
};
var __toModule = (module2) => {
  return __reExport(__markAsModule(__defProp(module2 != null ? __create(__getProtoOf(module2)) : {}, "default", module2 && module2.__esModule && "default" in module2 ? { get: () => module2.default, enumerable: true } : { value: module2, enumerable: true })), module2);
};

// src/widget.ts
__export(exports, {
  GoslingWidget: () => GoslingWidget
});
var import_base = __toModule(require("@jupyter-widgets/base"));
var import_jupyter_gosling = __toModule(require("nbextensions/jupyter-gosling/index"));
var GoslingWidget = class extends import_base.DOMWidgetView {
  viewElement = document.createElement("div");
  errorElement = document.createElement("div");
  render() {
    this.el.appendChild(this.viewElement);
    this.errorElement.style.color = "red";
    this.el.appendChild(this.errorElement);
    const reembed = () => {
      this.embed().catch((err) => console.error(err));
    };
    this.model.on("change:_spec_source", reembed);
    this.model.on("change:_opt_source", reembed);
    reembed();
  }
  async embed() {
    const spec = JSON.parse(this.model.get("_spec_source"));
    const opt = JSON.parse(this.model.get("_opt_source")) || {};
    if (spec == null)
      return;
    (0, import_jupyter_gosling.goslingEmbed)(this.viewElement, spec, opt);
  }
};

});
