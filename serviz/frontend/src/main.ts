import "./socketManager";
import { GoldenLayout, LayoutConfig } from "golden-layout";
import "./styles.css";
import { loadComponents } from "./loadComponents.ts";
import { loadLayouts } from "./layout_templates/load_layout.ts";
import DefaultConfig from "./layout_templates/Only field.json";

const menuContainerElement = document.querySelector("#menuContainer");
const layoutElement: HTMLElement | null =
  document.querySelector("#layoutContainer");

if (menuContainerElement && layoutElement) {
  const goldenLayout = new GoldenLayout(layoutElement);

  var savedState = localStorage.getItem("savedState");
  var layoutConfig: LayoutConfig = LayoutConfig.fromResolved(
    DefaultConfig as any
  );

  if (savedState) {
    console.log("Previous state restored");
    const resolvedConfig = JSON.parse(savedState);
    layoutConfig = LayoutConfig.fromResolved(resolvedConfig);
  } else {
    console.log("No saved state, loading default layout");
  }

  const [components, custom_components] = loadComponents();

  console.log(
    "All components that could be found:",
    components,
    custom_components
  );

  components.forEach((c) => {
    goldenLayout.registerComponentFactoryFunction(
      c.name,
      (glContainer: any, state: any) => {
        const cleanup = c.factory({ element: glContainer.element });

        if (typeof cleanup === "function") {
          glContainer.on("destroy", cleanup);
        }
      }
    );

    const newItem = document.createElement("li");
    newItem.textContent = c.name;
    menuContainerElement.appendChild(newItem);

    goldenLayout.newDragSource(newItem, c.name, c.factory);
  });

  if (custom_components.length > 0) {
    const customLabel = document.createElement("h3");
    customLabel.style.marginTop = "10px";
    customLabel.textContent = "Custom components:";
    menuContainerElement.appendChild(customLabel);
  }

  custom_components.forEach((c) => {
    goldenLayout.registerComponentFactoryFunction(
      c.name,
      (glContainer: any, state: any) => {
        const cleanup = c.factory({ element: glContainer.element });

        if (typeof cleanup === "function") {
          glContainer.on("destroy", cleanup);
        }
      }
    );

    const newItem = document.createElement("li");
    newItem.textContent = c.name;
    menuContainerElement.appendChild(newItem);

    goldenLayout.newDragSource(newItem, c.name, c.factory);
  });

  loadLayouts(goldenLayout);

  window.addEventListener("resize", () => {
    goldenLayout.updateRootSize();
  });

  goldenLayout.on("stateChanged", function () {
    // Delete popout buttons
    document.querySelectorAll(".lm_popout").forEach((el) => {
      el.remove();
    });

    const state = goldenLayout.saveLayout();
    localStorage.setItem("savedState", JSON.stringify(state));
  });

  try {
    goldenLayout.loadLayout(layoutConfig);
  } catch (err) {
    goldenLayout.loadLayout(LayoutConfig.fromResolved(DefaultConfig as any));
    console.warn("Error in saved state, loading default layout");
  }
}
