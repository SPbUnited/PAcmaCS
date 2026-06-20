import Component from "../loadComponents";

const guide = {
  en: {
    title: "Serviz guide",
    intro: `Drag components from the menu on the right, arrange them as needed, and resize panels by dragging their borders
Ready-made layouts are available at the bottom of the panel and can be loaded by clicking their names
Layout changes are saved in the cache so that they are preserved when the page is reloaded`,
    headings: ["Shortcut", "Action", "Context"],
    hotkeys: [
      [
        "Click a robot",
        "Select a robot for relocation (information about the robot will appear in the bottom-right corner)",
        "Field",
      ],
      ["Escape", "Clear the robot selected for relocation", "Field"],
      [
        "Alt + drag",
        "Set the ball position and velocity from the drag vector",
        "Field",
      ],
      [
        "WASD",
        "Move the selected robot",
        "SimControl (when Robot control is enabled)",
      ],
      [
        "Q E",
        "Rotate the selected robot",
        "SimControl (when Robot control is enabled)",
      ],
    ],
    details: `Field
Displays the field, robots, ball, and drawing layers. Drag the field to pan, use the mouse wheel to zoom, and click a robot to relocate it

SimControl
Controls simulator formations and individual robots. Enable Robot control before using the movement shortcuts

Telemetry
Telemetry displays incoming data

DrawingLayers
DrawingLayers lets you show, hide, reorder, and clear visual layers

PlaybackControl
Controls match recording and playback (records all drawing layers and telemetry to a file and lets you play them back)`,
  },
  ru: {
    title: "Гайд по Serviz",
    intro: `Перетаскивайте компоненты из правого меню, располагайте их удобным образом и изменяйте размер панелей, потянув за границу
В нижней части панели есть готовые раскладки, которые можно загрузить кликом по названию
При изменении раскладки она сохраняется в кеш, чтобы не сброситься при перезагрузке страницы`,
    headings: ["Сочетание", "Действие", "Контекст"],
    hotkeys: [
      [
        "Click on robot",
        "Выбрать робота для перемещения (справа снизу появится информация о роботе)",
        "Field",
      ],
      ["Escape", "Снять выбор робота для перемещения", "Field"],
      [
        "Alt + перетаскивание",
        "Задать положение и скорость мяча вектором перетаскивания",
        "Field",
      ],
      [
        "WASD",
        "Перемещать выбранного робота",
        "SimControl (при включённом Robot control)",
      ],
      [
        "Q E",
        "Вращать выбранного робота",
        "SimControl (при включённом Robot control)",
      ],
    ],
    details: `Field
Показывает поле, роботов, мяч и слои отрисовки. Перетаскивайте поле для перемещения, используйте колесо мыши для масштаба и нажмите на робота, чтобы изменить его положение

SimControl
Управляет расстановками симулятора и отдельными роботами. Перед использованием клавиш перемещения включите Robot control

Telemetry
Telemetry показывает входящие данные

DrawingLayers
DrawingLayers позволяет отображать, скрывать, переставлять и очищать визуальные слои

PlaybackControl
Управляет записью и воспроизведением матчей (записывает все слои отрисовки и телеметрию в файл, позволяет воспроизводить их)`,
  },
};

const Hotkeys: Component = {
  name: "Guide+Hotkeys",
  menuOrder: 100,
  factory: (container) => {
    container.element.style.background = "#1d1d1d";
    container.element.style.color = "#b0b0b0";
    container.element.style.font = "Arial, sans-serif";
    container.element.style.overflowY = "auto";

    const headerBar = document.createElement("div");
    headerBar.style.display = "flex";
    headerBar.style.alignItems = "center";
    headerBar.style.justifyContent = "space-between";
    headerBar.style.gap = "12px";
    headerBar.style.padding = "6px 10px";
    headerBar.style.background = "#1a1a1a";
    headerBar.style.width = "100%";
    headerBar.style.boxSizing = "border-box";
    container.element.appendChild(headerBar);

    const title = document.createElement("h3");
    title.style.margin = "0";
    title.style.flex = "1";
    headerBar.appendChild(title);

    const languageSwitch = createLanguageSwitch();
    headerBar.appendChild(languageSwitch.element);

    const intro = createTextBlock("");
    container.element.appendChild(intro);

    const table = document.createElement("table");
    table.style.width = "100%";
    table.style.borderCollapse = "collapse";

    const header = document.createElement("tr");
    const headerCells: HTMLTableCellElement[] = [];
    for (let index = 0; index < 3; index++) {
      const cell = document.createElement("th");
      cell.style.padding = "8px";
      cell.style.textAlign = "left";
      cell.style.borderBottom = "1px solid #444";
      header.appendChild(cell);
      headerCells.push(cell);
    }
    table.appendChild(header);

    const hotkeyCells: HTMLTableCellElement[][] = [];
    for (let rowIndex = 0; rowIndex < guide.en.hotkeys.length; rowIndex++) {
      const row = document.createElement("tr");
      const cells: HTMLTableCellElement[] = [];
      for (let columnIndex = 0; columnIndex < 3; columnIndex++) {
        const cell = document.createElement("td");
        cell.style.padding = "8px";
        cell.style.verticalAlign = "top";
        cell.style.borderBottom = "1px solid #333";
        row.appendChild(cell);
        cells.push(cell);
      }
      table.appendChild(row);
      hotkeyCells.push(cells);
    }

    container.element.appendChild(table);

    const details = createTextBlock("");
    container.element.appendChild(details);

    const setLanguage = (language: keyof typeof guide) => {
      const content = guide[language];
      title.textContent = content.title;
      intro.textContent = content.intro;
      details.textContent = content.details;
      headerCells.forEach((cell, index) => {
        cell.textContent = content.headings[index];
      });
      hotkeyCells.forEach((cells, rowIndex) => {
        cells.forEach((cell, columnIndex) => {
          cell.textContent = content.hotkeys[rowIndex][columnIndex];
        });
      });
      languageSwitch.setLanguage(language);
    };

    languageSwitch.element.addEventListener("click", () => {
      setLanguage(languageSwitch.language === "en" ? "ru" : "en");
    });
    setLanguage("en");
  },
};

export default Hotkeys;

function createTextBlock(text: string): HTMLDivElement {
  const block = document.createElement("div");
  block.textContent = text;
  block.style.padding = "12px";
  block.style.lineHeight = "1.5";
  block.style.whiteSpace = "pre-line";
  return block;
}

function createLanguageSwitch() {
  const element = document.createElement("button");
  element.type = "button";
  element.setAttribute("role", "switch");
  element.setAttribute("aria-label", "Guide language");
  element.style.display = "flex";
  element.style.alignItems = "center";
  element.style.flex = "0 0 auto";
  element.style.gap = "8px";
  element.style.margin = "0 0 0 auto";
  element.style.padding = "4px 8px";
  element.style.width = "auto";
  element.style.border = "0";
  element.style.background = "transparent";
  element.style.color = "#b0b0b0";
  element.style.cursor = "pointer";

  const enLabel = document.createElement("span");
  enLabel.textContent = "EN";
  element.appendChild(enLabel);

  const track = document.createElement("span");
  track.style.position = "relative";
  track.style.width = "36px";
  track.style.height = "20px";
  track.style.borderRadius = "10px";
  track.style.background = "#555";
  element.appendChild(track);

  const thumb = document.createElement("span");
  thumb.style.position = "absolute";
  thumb.style.top = "2px";
  thumb.style.left = "2px";
  thumb.style.width = "16px";
  thumb.style.height = "16px";
  thumb.style.borderRadius = "50%";
  thumb.style.background = "#ddd";
  thumb.style.transition = "transform 150ms ease";
  track.appendChild(thumb);

  const ruLabel = document.createElement("span");
  ruLabel.textContent = "RU";
  element.appendChild(ruLabel);

  let language: keyof typeof guide = "en";
  return {
    element,
    get language() {
      return language;
    },
    setLanguage(nextLanguage: keyof typeof guide) {
      language = nextLanguage;
      const isRussian = language === "ru";
      element.setAttribute("aria-checked", String(isRussian));
      thumb.style.transform = isRussian ? "translateX(16px)" : "none";
      enLabel.style.color = isRussian ? "#777" : "#fff";
      ruLabel.style.color = isRussian ? "#fff" : "#777";
    },
  };
}
