import Component from "../loadComponents";
import { bus, subscribeToTopic, sendMessage } from "../socketManager";
import { CustomDropdown } from "../customButtons";

const Telemetry: Component = {
  name: "Telemetry",
  factory: (container) => {
    container.element.style.display = "flex";
    container.element.style.flexDirection = "column";
    container.element.style.height = "100%";

    const wrapper = document.createElement("div");
    wrapper.style.display = "flex";
    wrapper.style.alignItems = "center";
    wrapper.style.padding = "5px";

    const selectDropdown = new CustomDropdown({
      options: [],
      onChange: (value) => {
        currentTopic = value;
        telemetryBox.textContent = getText(currentTopic);
      },
    });
    wrapper.appendChild(selectDropdown.element);

    const clearButton = document.createElement("button");
    clearButton.textContent = "Clear telemetry";
    clearButton.style.height = "30px";
    clearButton.style.width = "100px";
    clearButton.style.flex = "0 0 auto";
    clearButton.style.margin = "1px 10px 0px 10px ";
    wrapper.appendChild(clearButton);

    container.element.appendChild(wrapper);

    const telemetryBox = document.createElement("pre");
    telemetryBox.style.flexGrow = "1";
    container.element.appendChild(telemetryBox);

    let currentTopic = "";
    let telemetryData: Record<string, any> = {};

    function getText(currentTopic: string): string {
      if (currentTopic in telemetryData) {
        const data = telemetryData[currentTopic];
        if (typeof data === "string") {
          return data;
        } else {
          return JSON.stringify(data, null, 2);
        }
      }
      return "No telemetry right now";
    }

    subscribeToTopic("update_telemetry");

    bus.on("update_telemetry", (data) => {
      telemetryData = data;

      const previousTopic = currentTopic;
      const newOptions = Object.keys(data).map((t) => ({ value: t }));

      selectDropdown.updateOptions(newOptions);

      if (previousTopic && data[previousTopic] !== undefined) {
        currentTopic = previousTopic;
      } else if (newOptions.length > 0) {
        currentTopic = newOptions[0].value;
      }

      selectDropdown.updateOptions(newOptions);
      telemetryBox.textContent = getText(currentTopic);
    });

    clearButton.addEventListener("click", () => {
      sendMessage("clear_telemetry", "");
      currentTopic = "";
      selectDropdown.updateOptions([]);
      telemetryBox.textContent = "No telemetry right now";
    });
  },
};

export default Telemetry;
