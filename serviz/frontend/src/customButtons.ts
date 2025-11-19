type Option = {
  value: string;
};

type DropdownProps = {
  options: Option[];
  selected?: string;
  onChange?: (value: string) => void;
};

export class CustomDropdown {
  element: HTMLDivElement;
  private options: Option[];
  private selected: string;
  private onChange?: (value: string) => void;
  private dropdownList: HTMLDivElement;
  private isOpen: boolean = false;

  constructor({ options, selected, onChange }: DropdownProps) {
    this.options = options;
    this.selected = selected || options[0]?.value || "";
    this.onChange = onChange;

    this.element = document.createElement("div");
    this.element.style.position = "relative";
    this.element.style.display = "flex";
    this.element.style.flexDirection = "row";
    this.element.style.height = "30px";
    this.element.style.width = "calc(100% - 120px)";
    this.element.style.userSelect = "none";

    const selectedDiv = document.createElement("div");
    selectedDiv.textContent = this.selected;
    selectedDiv.style.padding = "5px 10px";
    selectedDiv.style.color = "#b0b0b0";
    selectedDiv.style.background = "#1a1a1a";
    selectedDiv.style.border = "1px solid #222";
    selectedDiv.style.cursor = "pointer";
    selectedDiv.style.flex = "1 1 auto";
    selectedDiv.style.whiteSpace = "nowrap";
    selectedDiv.style.overflow = "hidden";
    selectedDiv.style.textOverflow = "ellipsis";
    this.element.appendChild(selectedDiv);

    this.dropdownList = document.createElement("div");
    this.dropdownList.style.position = "absolute";
    this.dropdownList.style.top = "100%";
    this.dropdownList.style.left = "0";
    this.dropdownList.style.width = "100%";
    this.dropdownList.style.color = "#b0b0b0";
    this.dropdownList.style.background = "#1a1a1a";
    this.dropdownList.style.border = "1px solid #222";
    this.dropdownList.style.display = "none";
    this.dropdownList.style.zIndex = "1000";
    this.dropdownList.style.whiteSpace = "nowrap";
    this.dropdownList.style.overflow = "hidden";
    this.dropdownList.style.textOverflow = "ellipsis";
    this.element.appendChild(this.dropdownList);

    selectedDiv.addEventListener("mousedown", () => {
      this.isOpen = !this.isOpen;
      this.dropdownList.style.display = this.isOpen ? "block" : "none";
    });

    document.addEventListener("click", (e) => {
      if (!this.element.contains(e.target as Node)) {
        this.isOpen = false;
        this.dropdownList.style.display = "none";
      }
    });
    this.updateOptions(options);
  }

  public updateOptions(newOptions: Option[]) {
    const existingValues = this.options.map((o) => o.value);
    const incomingValues = newOptions.map((o) => o.value);

    this.options = this.options.filter((o) => incomingValues.includes(o.value));

    newOptions.forEach((o) => {
      if (!existingValues.includes(o.value)) {
        this.options.push(o);
      }
    });

    if (!this.options.some((o) => o.value === this.selected)) {
      this.selected = this.options[0]?.value || "";
    }

    (this.element.firstChild as HTMLDivElement).textContent = this.selected;

    this.dropdownList.innerHTML = "";
    this.options.forEach((opt) => {
      const div = document.createElement("div");
      div.textContent = opt.value;
      div.style.padding = "5px 10px";
      div.style.cursor = "pointer";

      div.addEventListener("mouseenter", () => {
        div.style.background = "#333";
      });
      div.addEventListener("mouseleave", () => {
        div.style.background = "#1a1a1a";
      });
      div.addEventListener("mouseup", () => {
        this.selected = opt.value;
        (this.element.firstChild as HTMLDivElement).textContent = this.selected;
        this.dropdownList.style.display = "none";
        this.isOpen = false;
        this.onChange?.(this.selected);
      });

      this.dropdownList.appendChild(div);
    });
  }

  public getValue() {
    return this.selected;
  }
}

export class NumberInput {
  element: HTMLDivElement;
  private input: HTMLInputElement;
  private upButton: HTMLButtonElement;
  private downButton: HTMLButtonElement;

  constructor(initialValue: number = 0) {
    this.element = document.createElement("div");
    this.element.style.position = "relative";
    this.element.style.display = "flex";
    this.element.style.height = "30px";
    this.element.style.width = "120px";
    this.element.style.userSelect = "none";

    this.input = document.createElement("input");
    this.input.style.color = "#b0b0b0";
    this.input.style.background = "#1a1a1a";
    this.input.style.padding = "5px";
    this.input.style.border = "1px solid #222";
    this.input.type = "number";
    this.input.value = "0";
    this.input.min = "0";
    this.input.max = "15";
    this.input.style.width = "100%";
    this.input.style.font = "18px Arial, sans-serif";
    this.input.style.outline = "none";

    this.input.addEventListener("input", () => {
      let value = Number(this.input.value);
      if (isNaN(value)) value = 0;
      value = Math.min(Math.max(value, 0), 15);
      this.input.value = value.toString();
    });

    this.element.appendChild(this.input);
  }
  public getValue() {
    return this.input.value;
  }
}
