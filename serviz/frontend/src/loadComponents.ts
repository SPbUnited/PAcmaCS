export function loadComponents() {
  const result: Component[] = [];

  const modules = import.meta.glob("./components/*.ts", { eager: true });
  for (const path in modules) {
    const mod: any = modules[path];
    if (mod.default) {
      result.push(mod.default);
    }
  }

  const custom_modules = import.meta.glob("../../../plugins/serviz/*.ts", {
    eager: true,
  });

  console.log("Found custom components:", custom_modules);
  for (const path in custom_modules) {
    const mod: any = custom_modules[path];
    if (mod.default) {
      result.push(mod.default);
    }
  }

  return result;
}

interface Component {
  name: string;
  factory: (container: { element: HTMLElement }) => void | (() => void);
  // returns unsubscribe function for every topic (bus.on)
}

export default Component;
