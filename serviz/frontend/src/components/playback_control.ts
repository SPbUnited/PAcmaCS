// тупо завайбкоженый код, пните меня если это оказалось в проде

import Component from "../loadComponents";
import { bus, subscribeToTopic, sendMessage } from "../socketManager";
import { CustomDropdown } from "../customButtons";

const PlaybackControls: Component = {
  name: "Playback",
  factory: (container) => {
    container.element.style.display = "flex";
    container.element.style.flexDirection = "column";
    container.element.style.height = "100%";
    container.element.style.padding = "8px";
    container.element.style.boxSizing = "border-box";

    function createWideButton(label: string, onClick: () => void): HTMLButtonElement {
      const btn = document.createElement("button");
      btn.className = "button-4 wide";
      btn.textContent = label;
      btn.style.marginBottom = "4px";
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        onClick();
      });
      return btn;
    }

    // --- Верхний блок кнопок ---

    const topButtons = document.createElement("div");
    topButtons.style.display = "flex";
    topButtons.style.flexDirection = "column";
    topButtons.style.marginBottom = "8px";

    // Reset view — здесь просто шлём сигнал, чтобы ты потом подключил обработку
    const resetViewButton = createWideButton("Reset view", () => {
      sendMessage("send_signal", { transnet: "reset_view" });
    });
    topButtons.appendChild(resetViewButton);

    const testButton = createWideButton("Test button", () => {
      sendMessage("send_signal", { transnet: "test_signal" });
    });
    topButtons.appendChild(testButton);

    const startRecordingButton = createWideButton("Start recording", () => {
      sendMessage("send_signal", { telsink: "start_recording" });
    });
    topButtons.appendChild(startRecordingButton);

    const stopRecordingButton = createWideButton("Stop recording", () => {
      sendMessage("send_signal", { telsink: "stop_recording" });
    });
    topButtons.appendChild(stopRecordingButton);

    const etherSelectButton = createWideButton("Ether select", () => {
      sendMessage("send_signal", { transnet: "ether_select" });
    });
    topButtons.appendChild(etherSelectButton);

    const phantomSelectButton = createWideButton("Phantom select", () => {
      sendMessage("send_signal", { transnet: "phantom_select" });
    });
    topButtons.appendChild(phantomSelectButton);

    container.element.appendChild(topButtons);

    // --- Блок выбора лога и управления проигрыванием ---

    const logControls = document.createElement("div");
    logControls.style.display = "flex";
    logControls.style.flexDirection = "column";
    logControls.style.gap = "6px";
    logControls.style.marginBottom = "8px";

    let currentLog = "";
    let logList: string[] = [];

    const logDropdown = new CustomDropdown({
      options: [],
      onChange: (value) => {
        currentLog = value;
      },
    });
    logControls.appendChild(logDropdown.element);

    const playbackButtonsRow = document.createElement("div");
    playbackButtonsRow.style.display = "flex";
    playbackButtonsRow.style.flexDirection = "row";
    playbackButtonsRow.style.justifyContent = "space-between";

    const startPlaybackButton = document.createElement("button");
    startPlaybackButton.className = "button-4";
    startPlaybackButton.textContent = "Start";
    startPlaybackButton.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!currentLog) return;
      sendMessage("send_signal", {
        telsink: "start_playback",
        data: currentLog,
      });
    });

    const pausePlaybackButton = document.createElement("button");
    pausePlaybackButton.className = "button-4";
    pausePlaybackButton.textContent = "Pause";
    pausePlaybackButton.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      sendMessage("send_signal", { telsink: "toggle_pause" });
    });

    const stopPlaybackButton = document.createElement("button");
    stopPlaybackButton.className = "button-4";
    stopPlaybackButton.textContent = "Stop";
    stopPlaybackButton.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      sendMessage("send_signal", { telsink: "stop_playback" });
    });

    playbackButtonsRow.appendChild(startPlaybackButton);
    playbackButtonsRow.appendChild(pausePlaybackButton);
    playbackButtonsRow.appendChild(stopPlaybackButton);

    logControls.appendChild(playbackButtonsRow);

    // --- Слайдер скорости воспроизведения ---

    let playbackSpeed = 1;

    const speedLabel = document.createElement("div");
    speedLabel.textContent = `Playback speed: ${playbackSpeed.toFixed(1)}`;
    logControls.appendChild(speedLabel);

    const speedSlider = document.createElement("input");
    speedSlider.type = "range";
    speedSlider.min = "0.2";
    speedSlider.max = "2";
    speedSlider.step = "0.2";
    speedSlider.value = String(playbackSpeed);
    speedSlider.style.width = "100%";

    speedSlider.addEventListener("change", () => {
      playbackSpeed = parseFloat(speedSlider.value);
      if (Number.isNaN(playbackSpeed)) playbackSpeed = 1;
      speedLabel.textContent = `Playback speed: ${playbackSpeed.toFixed(1)}`;
      sendMessage("send_signal", {
        telsink: "set_playback_speed",
        data: playbackSpeed,
      });
    });

    logControls.appendChild(speedSlider);

    // --- Кнопка Move forward 10s ---

    const moveForwardButton = document.createElement("button");
    moveForwardButton.className = "button-4";
    moveForwardButton.textContent = "Move forward 10s";
    moveForwardButton.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      sendMessage("send_signal", {
        telsink: "move_forward",
        data: 10,
      });
    });

    logControls.appendChild(moveForwardButton);

    container.element.appendChild(logControls);

    // --- Подписка на список логов от бэка ---

    subscribeToTopic("update_telsink_log_list");

    const onUpdateLogList = (data: string[]) => {
      if (!Array.isArray(data)) return;

      logList = data.map((x) => String(x));

      const options = logList.map((log) => ({ value: log }));
      logDropdown.updateOptions(options);

      if (!currentLog || !logList.includes(currentLog)) {
        currentLog = logList[0] ?? "";
      }
    };

    bus.on("update_telsink_log_list", onUpdateLogList);

    return () => {
      bus.off("update_telsink_log_list", onUpdateLogList);
    };
  },
};

export default PlaybackControls;
