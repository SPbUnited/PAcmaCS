import "./socketManager";
import { GoldenLayout, LayoutConfig } from "golden-layout";
import "./styles.css";
import { loadComponents } from "./loadComponents.js";

const menuContainerElement = document.querySelector("#menuContainer");
const layoutElement: HTMLElement | null =
  document.querySelector("#layoutContainer");

if (menuContainerElement && layoutElement) {
  const goldenLayout = new GoldenLayout(layoutElement);

  const defaultConfig: LayoutConfig = {
    root: {
      type: "row",
      content: [],
    },
  };

  var savedState = localStorage.getItem("savedState");
  var layoutConfig: LayoutConfig;

  if (savedState) {
    console.log("Previous state restored");
    const resolvedConfig = JSON.parse(savedState);
    layoutConfig = LayoutConfig.fromResolved(resolvedConfig);
  } else {
    console.log("No saved state, loading default layout");
    layoutConfig = defaultConfig;
  }

  const components = loadComponents();

  console.log("All components that could be found:", components);

  components.forEach((c) => {
    goldenLayout.registerComponentFactoryFunction(c.name, c.factory);

    const newItem = document.createElement("li");
    newItem.textContent = c.name;
    menuContainerElement.appendChild(newItem);

    goldenLayout.newDragSource(newItem, c.name, c.factory);
  });

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

  goldenLayout.loadLayout(layoutConfig);
}
