import Component from "../loadComponents";
import { sendMessage } from "../socketManager";

function parseHexToBytes(hex: string): number[] {
  const cleaned = hex.replace(/[^0-9a-fA-F]/g, "");
  if (!cleaned.length) {
    throw new Error("Введите пакет NRFM в шестнадцатеричном виде");
  }
  if (cleaned.length % 2 !== 0) {
    throw new Error("Нечётное количество hex-символов");
  }

  const bytes: number[] = [];
  for (let i = 0; i < cleaned.length; i += 2) {
    const byte = parseInt(cleaned.slice(i, i + 2), 16);
    if (Number.isNaN(byte)) {
      throw new Error("Ошибка разбора hex-строки");
    }
    bytes.push(byte);
  }
  return bytes;
}

function buildUdpieDebugOverride(nrfmHex: string): number[] {
  const nrfmBytes = parseHexToBytes(nrfmHex);

  const preamble = nrfmBytes[0];
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

    const label = document.createElement("h3");
    label.textContent = "NRFM debug_override пакет (hex, без байта 0xDE):";
    label.style.marginBottom = "4px";
    container.element.appendChild(label);

    const input = document.createElement("textarea");
    input.style.width = "100%";
    input.style.height = "80px";
    input.style.resize = "vertical";
    input.style.fontFamily = "monospace";
    input.placeholder = "Например: A8 0A 00";
    container.element.appendChild(input);

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
        const udpBytes = buildUdpieDebugOverride(input.value);

        const packet = {
          control: "send_udpie",
          data: udpBytes,
        };

        sendMessage("send_signal", packet);

        const hexString = udpBytes
          .map((b) => b.toString(16).padStart(2, "0").toUpperCase())
          .join(" ");
        status.style.color = "#88dd00";
        status.textContent = `Отправлено: ${hexString}`;
      } catch (err) {
        const msg = err instanceof Error ? err.message : "Неизвестная ошибка";
        status.style.color = "#ff5555";
        status.textContent = msg;
      }
    });

    return () => {};
  },
};

export default SendUdpie;
