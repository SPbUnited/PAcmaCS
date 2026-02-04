import Component from "../loadComponents";
import { bus, subscribeToTopic, sendMessage } from "../socketManager";
import { CustomDropdown } from "../customButtons";

const PlaybackControls: Component = {
  name: "Playback",
  factory: (container) => {
    const root = container.element;
    root.style.display = "flex";
    root.style.flexDirection = "column";
    root.style.height = "100%";
    root.style.padding = "8px";
    root.style.boxSizing = "border-box";
    root.style.gap = "8px";

    const row = () => {
      const d = document.createElement("div");
      d.style.display = "flex";
      d.style.gap = "6px";
      return d;
    };

    const btn = (label: string, wide: boolean = false) => {
      const b = document.createElement("button");
      if (wide) {
        b.style.width = "50%";
        b.style.marginLeft = "0px";
        b.style.marginRight = "0px";
        b.style.height = "40px";
        b.style.fontSize = "20px";
      }
      b.textContent = label;
      return b;
    };

    // =====================================================
    // Switch Ether / Phantom
    // =====================================================

    const netRow = row();

    const etherBtn = btn("Switch to LIVE data", false);
    etherBtn.onclick = () => {
      sendMessage("send_signal", { transnet: "ether_select" });
      if (autoSwitchCheckbox.checked) {
        sendMessage("clear_layers", "");
        sendMessage("clear_telemetry", "");
      }
    };

    const phantomBtn = btn("Switch to LOG replay", false);
    phantomBtn.onclick = () => {
      sendMessage("send_signal", { transnet: "phantom_select" });
      if (autoSwitchCheckbox.checked) {
        sendMessage("clear_layers", "");
        sendMessage("clear_telemetry", "");
      }
    };

    netRow.append(etherBtn, phantomBtn);
    root.appendChild(netRow);

    const checkboxRow = document.createElement("label");
    checkboxRow.style.display = "flex";
    checkboxRow.style.alignItems = "center";
    checkboxRow.style.justifyContent = "center";
    checkboxRow.style.gap = "6px";
    checkboxRow.style.fontSize = "14px";
    checkboxRow.style.opacity = "0.8";

    const autoSwitchCheckbox = document.createElement("input");
    autoSwitchCheckbox.type = "checkbox";
    autoSwitchCheckbox.checked = true; // по умолчанию

    const checkboxText = document.createElement("span");
    checkboxText.textContent = "Auto clear telemetry and drawing layers";

    checkboxRow.append(autoSwitchCheckbox, checkboxText);
    root.appendChild(checkboxRow);

    // =====================================================
    // Mode selector
    // =====================================================

    let mode: "recording" | "playing" = "recording";

    const modeRow = row();

    const recordingTab = btn("Recording", true);
    const playingTab = btn("Playing", true);

    recordingTab.style.flex = "1";
    recordingTab.style.width = "50%";
    playingTab.style.flex = "1";

    const updateModeUI = () => {
      recordingTab.style.opacity = mode === "recording" ? "1" : "0.4";
      playingTab.style.opacity = mode === "playing" ? "1" : "0.4";
      recordingBlock.style.display = mode === "recording" ? "block" : "none";
      playingBlock.style.display = mode === "playing" ? "block" : "none";
      recordingTab.style.fontWeight = mode === "recording" ? "600" : "400";
      playingTab.style.fontWeight = mode === "playing" ? "600" : "400";
    };

    recordingTab.onclick = () => {
      mode = "recording";
      updateModeUI();
    };

    playingTab.onclick = () => {
      mode = "playing";
      updateModeUI();
    };

    modeRow.append(recordingTab, playingTab);
    root.appendChild(modeRow);

    // =====================================================
    // Recording block
    // =====================================================

    let isRecording = false;

    const recordingBlock = document.createElement("div");

    const recordBtn = btn("Start recording", false);
    recordBtn.onclick = () => {
      sendMessage("send_signal", {
        telsink: isRecording ? "stop_recording" : "start_recording",
      });
    };
    recordBtn.style.width = "250px";
    recordBtn.style.marginLeft = "auto";
    recordBtn.style.marginRight = "auto";

    recordingBlock.appendChild(recordBtn);
    root.appendChild(recordingBlock);

    // =====================================================
    // Playing block
    // =====================================================

    const playingBlock = document.createElement("div");
    playingBlock.style.display = "none";
    playingBlock.style.display = "flex";
    playingBlock.style.flexDirection = "column";
    playingBlock.style.gap = "6px";

    let currentLog = "";
    let logList: string[] = [];

    const logDropdown = new CustomDropdown({
      options: [],
      onChange: (v) => (currentLog = v),
    });

    playingBlock.appendChild(logDropdown.element);

    // --- play / pause / stop ---

    const playRow = row();

    const playBtn = btn("Play");
    playBtn.onclick = () => {
      if (!currentLog) return;
      sendMessage("send_signal", {
        telsink: "start_playback",
        data: currentLog,
      });
    };

    const pauseBtn = btn("Pause");
    pauseBtn.onclick = () =>
      sendMessage("send_signal", { telsink: "toggle_pause" });

    const stopBtn = btn("Stop");
    stopBtn.onclick = () => {
      sendMessage("send_signal", { telsink: "stop_playback" });
      if (autoSwitchCheckbox.checked) {
        sendMessage("clear_layers", "");
        sendMessage("clear_telemetry", "");
      }
    };

    playRow.append(playBtn, pauseBtn, stopBtn);
    playingBlock.appendChild(playRow);

    // --- status bar ---

    let currentTime = 0;
    let duration = 0;

    const timeBar = document.createElement("div");
    timeBar.style.position = "relative";
    timeBar.style.height = "16px";
    timeBar.style.background = "#333";
    timeBar.style.borderRadius = "4px";

    const fill = document.createElement("div");
    fill.style.height = "100%";
    fill.style.background = "#6cf";
    fill.style.width = "0%";
    fill.style.borderRadius = "4px";

    timeBar.appendChild(fill);

    const timeLeft = document.createElement("div");
    const timeRight = document.createElement("div");

    timeLeft.style.fontSize = timeRight.style.fontSize = "14px";
    timeLeft.style.color = timeRight.style.color = "#b0b0b0";
    timeLeft.style.textAlign = "left";
    timeRight.style.textAlign = "right";

    playingBlock.append(timeLeft, timeBar, timeRight);

    // --- speed (log scale) ---

    let speed = 1;

    const speedLabel = document.createElement("div");
    speedLabel.textContent = "Speed: 1.0x";
    speedLabel.style.color = "#b0b0b0";

    const speedSlider = document.createElement("input");
    speedSlider.type = "range";
    speedSlider.min = "0";
    speedSlider.max = "100";
    speedSlider.value = "50";
    speedSlider.style.width = "200%";

    speedSlider.oninput = () => {
      const t = Number(speedSlider.value) / 100;
      speed = Math.pow(10, t * 2 - 1); // 0.1 .. 10
      speedLabel.textContent = `Speed: ${speed.toFixed(2)}x`;
      sendMessage("send_signal", {
        telsink: "set_playback_speed",
        data: speed,
      });
    };

    // --- seek buttons ---

    const seekRow = row();

    const backBtn = btn("-10s");
    backBtn.onclick = () =>
      sendMessage("send_signal", { telsink: "move_forward", data: -10 });

    const forwardBtn = btn("+10s");
    forwardBtn.onclick = () =>
      sendMessage("send_signal", { telsink: "move_forward", data: 10 });

    seekRow.append(speedSlider, backBtn, forwardBtn);
    playingBlock.append(speedLabel);
    playingBlock.appendChild(seekRow);

    root.appendChild(playingBlock);

    updateModeUI();

    // =====================================================
    // Backend subscriptions
    // =====================================================

    subscribeToTopic("update_telsink_log_list");
    subscribeToTopic("update_telsink_recording_status");

    const onLogs = (data: string[]) => {
      if (!Array.isArray(data)) return;
      logList = data.map(String);
      logDropdown.updateOptions(logList.map((x) => ({ value: x })));
      if (!currentLog) currentLog = logList[0] ?? "";
    };

    const onStatus = (data: any) => {
      if (typeof data.isRecording === "boolean") {
        isRecording = data.isRecording;
        recordBtn.textContent = isRecording
          ? "Stop recording"
          : "Start recording";
      }

      if (typeof data.currentTime === "number") {
        currentTime = data.currentTime;
        timeLeft.textContent = `${currentTime.toFixed(1)}s`;
      }

      if (typeof data.duration === "number") {
        duration = data.duration;
        timeRight.textContent = `${duration.toFixed(1)}s`;
      }

      if (duration > 0) {
        fill.style.width = `${Math.min(100, (currentTime / duration) * 100)}%`;
      }
    };

    bus.on("update_telsink_log_list", onLogs);
    bus.on("update_telsink_recording_status", onStatus);

    return () => {
      bus.off("update_telsink_log_list", onLogs);
      bus.off("update_telsink_recording_status", onStatus);
    };
  },
};

export default PlaybackControls;
