import Component from "../loadComponents";
import { bus, subscribeToTopic, sendMessage } from "../socketManager";

const DrawingLayers: Component = {
  name: "Drawing layers",
  factory: (container) => {
    container.element.style.position = "relative";
    container.element.style.overflowY = "auto";

    const wrapper = document.createElement("div");
    wrapper.style.display = "flex";
    wrapper.style.alignItems = "center";
    wrapper.style.marginBottom = "1px";
    wrapper.style.background = "#1a1a1a";

    const upHeader = document.createElement("h3");
    upHeader.textContent = "Layers visibility settings:";
    upHeader.style.background = "none";
    upHeader.style.display = "flex";
    upHeader.style.flexDirection = "row";
    upHeader.style.height = "auto";
    upHeader.style.width = "calc(100% - 120px)";
    upHeader.style.userSelect = "none";
    wrapper.append(upHeader);

    const clearButton = document.createElement("button");
    clearButton.textContent = "Clear layers";
    clearButton.style.height = "30px";
    clearButton.style.width = "100px";
    clearButton.style.flex = "0 0 auto";
    clearButton.style.margin = "1px 10px 0px 10px ";
    wrapper.appendChild(clearButton);

    container.element.appendChild(wrapper);

    const layersList = document.createElement("div");
    layersList.style.padding = "10px";
    layersList.style.color = "#b0b0b0";
    layersList.style.background = "#1d1d1d";
    layersList.style.font = "Arial, sans-serif";
    container.element.append(layersList);

    function findCheckbox(name: string): HTMLInputElement | undefined {
      const items = layersList.querySelectorAll<HTMLInputElement>(
        'input[type="checkbox"][data-layer]'
      );
      for (const el of Array.from(items))
        if (el.dataset.layer === name) return el;
      return undefined;
    }
    subscribeToTopic("update_sprites");
    bus.on("update_sprites", (data) => {
      const validNames = new Set<string>();
      for (const layerName of Object.keys(data)) {
        const layer = data[layerName];
        if (!layer || !Array.isArray(layer.data)) continue;
        validNames.add(layerName);

        let checkbox = findCheckbox(layerName);
        if (!checkbox) {
          //Add new checkbox
          const label = document.createElement("label");
          label.style.display = "block";

          checkbox = document.createElement("input");
          checkbox.type = "checkbox";
          checkbox.checked = !!layer.is_visible;
          checkbox.dataset.level = layer.level ?? "0";
          checkbox.dataset.layer = layerName;

          checkbox.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopImmediatePropagation();
            sendMessage("toggle_layer_visibility", layerName);
          });

          label.appendChild(checkbox);
          label.appendChild(document.createTextNode(" " + layerName));
          layersList.appendChild(label);
        } else {
          checkbox.checked = !!layer.is_visible;
        }
      }

      const existing = layersList.querySelectorAll<HTMLLabelElement>("label");
      for (const label of Array.from(existing)) {
        const input = label.querySelector<HTMLInputElement>(
          'input[type="checkbox"][data-layer]'
        );
        const name = input?.dataset.layer;
        if (name && !validNames.has(name)) label.remove();
      }
    });
    clearButton.addEventListener("click", () => {
      sendMessage("clear_layers", "");
    });
  },
};

export default DrawingLayers;
