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

    const layerHeigh = new Map<string, number>();

    subscribeToTopic("update_sprites");
    const onUpdateSprites = (data) => {
      const validNames = new Set<string>();
      let update = false;
      for (const layerName of Object.keys(data)) {
        const layer = data[layerName];
        if (!layer || !Array.isArray(layer.data)) continue;
        validNames.add(layerName);

        const heighValue = Number(layer.heigh);
        if (layerHeigh.get(layerName) != heighValue) {
          update = true;
          layerHeigh.set(layerName, heighValue);
        }

        let checkbox = findCheckbox(layerName);
        if (!checkbox) {
          update = true;
          //Add new checkbox
          const label = document.createElement("label");
          label.style.display = "flex";
          label.style.alignItems = "center";
          label.style.marginBottom = "2px";
          label.style.width = "100%";
          label.dataset.layer = layerName;

          const leftPart = document.createElement("span");
          leftPart.style.display = "flex";
          leftPart.style.alignItems = "center";
          leftPart.style.flex = "1 1 auto";
          leftPart.style.minWidth = "0"; // важно для ellipsis в flex

          checkbox = document.createElement("input");
          checkbox.type = "checkbox";
          checkbox.checked = !!layer.is_visible;
          checkbox.dataset.level = layer.level ?? "0";
          checkbox.dataset.layer = layerName;
          checkbox.style.marginRight = "5px";

          checkbox.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopImmediatePropagation();
            sendMessage("toggle_layer_visibility", layerName);
          });

          // span для текста с обрезкой
          const nameSpan = document.createElement("span");
          nameSpan.textContent = " " + layerName;
          nameSpan.style.display = "inline-block";
          nameSpan.style.flex = "1 1 auto";
          nameSpan.style.minWidth = "0";
          nameSpan.style.whiteSpace = "nowrap";
          nameSpan.style.overflow = "hidden";
          nameSpan.style.textOverflow = "ellipsis";

          leftPart.appendChild(checkbox);
          leftPart.appendChild(nameSpan);

          const rightPart = document.createElement("span");
          rightPart.style.display = "flex";
          rightPart.style.gap = "2px"; // меньше расстояние между стрелками
          rightPart.style.marginLeft = "auto";
          rightPart.style.flexShrink = "0"; // не сжимать стрелки

          const buttonSize = "25px";

          const upButton = document.createElement("button");
          upButton.textContent = "↑";
          upButton.style.width = buttonSize;
          upButton.style.height = buttonSize;
          upButton.style.margin = "5px";
          upButton.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopImmediatePropagation();
            sendMessage("move_layer_up", layerName);
          });

          const downButton = document.createElement("button");
          downButton.textContent = "↓";
          downButton.style.width = buttonSize;
          downButton.style.height = buttonSize;
          downButton.style.margin = "5px";
          downButton.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopImmediatePropagation();
            sendMessage("move_layer_down", layerName);
          });

          rightPart.appendChild(upButton);
          rightPart.appendChild(downButton);

          label.appendChild(leftPart);
          label.appendChild(rightPart);

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

      for (const name of Array.from(layerHeigh.keys())) {
        if (!validNames.has(name)) {
          layerHeigh.delete(name);
        }
      }

      if (update) {
        const labels = Array.from(
          layersList.querySelectorAll<HTMLLabelElement>("label")
        );
        labels.sort((a, b) => {
          const aInput = a.querySelector<HTMLInputElement>(
            'input[type="checkbox"][data-layer]'
          );
          const bInput = b.querySelector<HTMLInputElement>(
            'input[type="checkbox"][data-layer]'
          );
          const aName = aInput?.dataset.layer ?? "";
          const bName = bInput?.dataset.layer ?? "";
          const aHeigh = layerHeigh.get(aName) ?? 0;
          const bHeigh = layerHeigh.get(bName) ?? 0;
          return aHeigh - bHeigh;
        });
        for (const label of labels) {
          layersList.appendChild(label);
        }
      }
    };

    bus.on("update_sprites", onUpdateSprites);
    clearButton.addEventListener("click", () => {
      sendMessage("clear_layers", "");
    });

    return () => {
      bus.off("update_sprites", onUpdateSprites);
    };
  },
};

export default DrawingLayers;
