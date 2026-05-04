import { GoldenLayout, LayoutConfig } from "golden-layout";

type LayoutItem = {
  name: string;
  config: unknown;
};

const jsonModules = import.meta.glob("./*.json", {
  eager: true
});

const layouts: LayoutItem[] = Object.entries(jsonModules).map(
  ([path, mod]) => {
    // path вида "./sim_half.json" → "sim_half"
    const fileName = path.split("/").pop() || "";
    const name = fileName.replace(/\.json$/, "");

    const config = (mod as any).default ?? mod;

    return { name, config };
  }
);

export function loadLayouts(goldenLayout: GoldenLayout) {
  const bottomMenuContainer =
    document.querySelector<HTMLUListElement>("#bottomMenuContainer");
  if (!bottomMenuContainer) {
    return;
  }

  layouts.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item.name;
    bottomMenuContainer.appendChild(li);

    li.addEventListener("click", () => {
      const cfg = LayoutConfig.fromResolved(item.config as any);
      goldenLayout.loadLayout(cfg);
    });
  });
}
