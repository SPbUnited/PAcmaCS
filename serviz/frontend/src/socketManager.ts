import { io } from "socket.io-client";
import { EventEmitter } from "events";

export const socket = io("http://localhost:8100");
export const bus = new EventEmitter();

socket.onAny((event, data) => {
  bus.emit(event, data);
});

socket.on("connect", () => console.log("Connected to backend"));
socket.on("disconnect", () => console.log("Disconnected from backend"));

export function subscribeToTopic(topic: string) {
  socket.on(topic, (payload) => {
    bus.emit(topic, payload);
  });
}

export function sendMessage(topic: string, payload: any) {
  socket.emit(topic, payload);
}
