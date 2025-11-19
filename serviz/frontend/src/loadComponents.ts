export function loadComponents() {
  const modules = import.meta.glob("./components/*.ts", { eager: true });
  const result: Component[] = [];

  for (const path in modules) {
    const mod: any = modules[path];
    if (mod.default) {
      result.push(mod.default);
    }
  }

  return result;
}

interface Component {
  name: string;
  factory: (container: { element: HTMLElement }) => void;
}

export default Component;
