import Component from "../loadComponents";
import { sendMessage } from "../socketManager";
import { CustomDropdown } from "../customButtons";

function parseNibble(hex1: string, fieldName: string): number {
  const cleaned = hex1.replace(/[^0-9a-fA-F]/g, "");
  if (cleaned.length !== 1) {
    throw new Error(`${fieldName}: нужно ввести ровно 1 hex-символ`);
  }
  const v = parseInt(cleaned, 16);
  if (Number.isNaN(v) || v < 0 || v > 0xf) {
    throw new Error(`${fieldName}: не удалось разобрать hex-значение`);
  }
  return v;
}

function parseByte2(hex2: string, fieldName: string): number {
  const cleaned = hex2.replace(/[^0-9a-fA-F]/g, "");
  if (cleaned.length !== 2) {
    throw new Error(
      `${fieldName}: нужно ввести ровно 2 шестнадцатеричных символа`
    );
  }
  const value = parseInt(cleaned, 16);
  if (Number.isNaN(value)) {
    throw new Error(`${fieldName}: не удалось разобрать hex-значение`);
  }
  return value;
}

function floatToBytes(value: number): number[] {
  const buf = new ArrayBuffer(4);
  const view = new DataView(buf);
  view.setFloat32(0, value, false);
  return [
    view.getUint8(0),
    view.getUint8(1),
    view.getUint8(2),
    view.getUint8(3),
  ];
}

function buildUdpieDebugOverride(
  typeNibbleHex: string,
  robotNibbleHex: string,
  deviceHex: string,
  regHex: string | null,
  drvIdHex: string | null,
  payloadText: string
): number[] {
  const typeNibble = parseNibble(typeNibbleHex, "Тип пакета");
  const robotNibble = parseNibble(robotNibbleHex, "Индекс робота");
  const preamble = (typeNibble << 4) | robotNibble;

  const deviceByte = parseByte2(deviceHex, "Устройство");
  const nrfmBytes: number[] = [preamble, deviceByte];

  const devUpper = deviceHex.toUpperCase();

  if (devUpper === "0A") {
    if (!regHex) {
      throw new Error("Регистр: нужно указать значение");
    }
    const regByte = parseByte2(regHex, "Регистр");
    nrfmBytes.push(regByte);
  } else if (devUpper === "0C") {
    if (!drvIdHex) {
      throw new Error("DRV ID: нужно указать значение");
    }
    if (!regHex) {
      throw new Error("Регистр: нужно указать значение");
    }
    const drvIdByte = parseByte2(drvIdHex, "DRV ID");
    const regByte = parseByte2(regHex, "Регистр");
    nrfmBytes.push(drvIdByte, regByte);
  }

  const trimmed = payloadText.trim();
  if (trimmed.length > 0) {
    const num = Number(trimmed.replace(",", "."));
    if (Number.isNaN(num)) {
      throw new Error("Полезная нагрузка: требуется число (например 0.2)");
    }
    const payloadBytes = floatToBytes(num);
    nrfmBytes.push(...payloadBytes);
  }

  const packetType = (preamble >> 4) & 0x0f;
  if (packetType !== 0x0a) {
    console.warn(
      "NRFM preamble не соответствует типу debug_override (ожидается 0xA?)"
    );
  }

  const udpBytes = [0xde, ...nrfmBytes];
  return udpBytes;
}

const SendUdpie: Component = {
  name: "Send Udpie",
  factory: (container) => {
    container.element.style.display = "flex";
    container.element.style.flexDirection = "column";
    container.element.style.height = "100%";
    container.element.style.padding = "8px";
    container.element.style.boxSizing = "border-box";

    const title = document.createElement("h3");
    title.textContent = "NRFM debug_override пакет (без байта 0xDE):";
    title.style.marginBottom = "8px";
    container.element.appendChild(title);

    const firstRow = document.createElement("div");
    firstRow.style.display = "flex";
    firstRow.style.alignItems = "flex-start";
    firstRow.style.gap = "8px";
    firstRow.style.marginBottom = "8px";

    // ---- Тип пакета ----
    const firstLabel = document.createElement("label");
    firstLabel.style.display = "flex";
    firstLabel.style.flexDirection = "column";
    firstLabel.style.alignItems = "flex-start";

    const firstLabelText = document.createElement("span");
    firstLabelText.textContent = "Тип пакета:";

    const firstInput = document.createElement("input");
    firstInput.type = "text";
    firstInput.maxLength = 1;
    firstInput.style.width = "22px";
    firstInput.style.fontFamily = "monospace";
    firstInput.placeholder = "A";

    firstLabel.appendChild(firstLabelText);
    firstLabel.appendChild(firstInput);

    // ---- Индекс робота ----
    const secondLabel = document.createElement("label");
    secondLabel.style.display = "flex";
    secondLabel.style.flexDirection = "column";
    secondLabel.style.alignItems = "flex-start";

    const secondLabelText = document.createElement("span");
    secondLabelText.textContent = "Индекс робота:";

    const secondInput = document.createElement("input");
    secondInput.type = "text";
    secondInput.maxLength = 1;
    secondInput.style.width = "22px";
    secondInput.style.fontFamily = "monospace";
    secondInput.placeholder = "8";

    secondLabel.appendChild(secondLabelText);
    secondLabel.appendChild(secondInput);

    // ---- Устройство (dropdown) ----
    const deviceLabel = document.createElement("label");
    deviceLabel.style.display = "flex";
    deviceLabel.style.flexDirection = "column";
    deviceLabel.style.alignItems = "flex-start";

    const deviceLabelText = document.createElement("span");
    deviceLabelText.textContent = "Устройство:";

    const deviceDropdown = new CustomDropdown({
      options: [],
      onChange: (value) => {
        currentDevice = value;
        updateDeviceFields();
      },
    });
    deviceDropdown.element.style.width = "auto";
    deviceDropdown.element.style.width = "50px";

    deviceLabel.appendChild(deviceLabelText);
    deviceLabel.appendChild(deviceDropdown.element);

    // ---- DRV ID ----
    const drvIdLabel = document.createElement("label");
    drvIdLabel.style.display = "flex";
    drvIdLabel.style.flexDirection = "column";
    drvIdLabel.style.alignItems = "flex-start";

    const drvIdLabelText = document.createElement("span");
    drvIdLabelText.textContent = "DRV ID:";

    const drvIdInput = document.createElement("input");
    drvIdInput.type = "text";
    drvIdInput.maxLength = 2;
    drvIdInput.style.width = "32px";
    drvIdInput.style.fontFamily = "monospace";
    drvIdInput.placeholder = "00";

    drvIdLabel.appendChild(drvIdLabelText);
    drvIdLabel.appendChild(drvIdInput);

    // ---- Регистр ----
    const regLabel = document.createElement("label");
    regLabel.style.display = "flex";
    regLabel.style.flexDirection = "column";
    regLabel.style.alignItems = "flex-start";

    const regLabelText = document.createElement("span");
    regLabelText.textContent = "Регистр:";

    const regInput = document.createElement("input");
    regInput.type = "text";
    regInput.maxLength = 2;
    regInput.style.width = "32px";
    regInput.style.fontFamily = "monospace";
    regInput.placeholder = "20";

    regLabel.appendChild(regLabelText);
    regLabel.appendChild(regInput);

    firstRow.appendChild(firstLabel);
    firstRow.appendChild(secondLabel);
    firstRow.appendChild(deviceLabel);
    firstRow.appendChild(drvIdLabel);
    firstRow.appendChild(regLabel);
    container.element.appendChild(firstRow);

    deviceDropdown.updateOptions([{ value: "0A" }, { value: "0C" }]);
    let currentDevice = "0A";

    function updateDeviceFields() {
      if (currentDevice === "0C") {
        drvIdLabel.style.display = "flex";
        regLabel.style.display = "flex";
      } else if (currentDevice === "0A") {
        drvIdLabel.style.display = "none";
        regLabel.style.display = "flex";
      } else {
        drvIdLabel.style.display = "none";
        regLabel.style.display = "none";
      }
    }


    updateDeviceFields();

    const payloadLabel = document.createElement("label");
    payloadLabel.textContent =
      "Полезная нагрузка (float, будет закодирована как float32):";
    payloadLabel.style.marginBottom = "4px";
    container.element.appendChild(payloadLabel);

    const payloadInput = document.createElement("textarea");
    payloadInput.style.width = "auto";
    payloadInput.style.height = "60px";
    payloadInput.style.resize = "vertical";
    payloadInput.style.fontFamily = "monospace";
    payloadInput.placeholder = "Например: 0.2";
    container.element.appendChild(payloadInput);

    const status = document.createElement("div");
    status.style.marginTop = "4px";
    status.style.fontSize = "12px";
    container.element.appendChild(status);

    const sendButton = document.createElement("button");
    sendButton.textContent = "Send UDPie";
    sendButton.style.marginTop = "8px";
    sendButton.style.height = "30px";
    sendButton.style.alignSelf = "flex-start";
    container.element.appendChild(sendButton);

    sendButton.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();

      status.textContent = "";
      status.style.color = "#b0b0b0";

      try {
        const udpBytes = buildUdpieDebugOverride(
          firstInput.value,
          secondInput.value,
          currentDevice,
          regInput.value,
          drvIdInput.value,
          payloadInput.value
        );

        const packet = {
          control: "send_udpie",
          data: udpBytes,
        };

        sendMessage("send_signal", packet);

        let headerLen = udpBytes.length;

        if (payloadInput.value.trim().length > 0) {
          if (currentDevice === "0A") {
            headerLen = 4;
          } else if (currentDevice === "0C") {
            headerLen = 5;
          }
        }

        const toHex = (b: number) => b.toString(16).padStart(2, "0").toUpperCase();

        const headerPart = udpBytes.slice(0, headerLen).map(toHex).join(" ");
        const payloadPart =
          headerLen < udpBytes.length
            ? udpBytes.slice(headerLen).map(toHex).join(" ")
            : "";

        const hexString =
          payloadPart.length > 0 ? `${headerPart} | ${payloadPart}` : headerPart;

        status.style.color = "#88dd00";
        status.textContent = `Отправлено: ${hexString}`;
      } catch (err) {
        const msg = err instanceof Error ? err.message : "Неизвестная ошибка";
        status.style.color = "#ff5555";
        status.textContent = msg;
      }
    });

    return () => { };
  },
};

export default SendUdpie;
