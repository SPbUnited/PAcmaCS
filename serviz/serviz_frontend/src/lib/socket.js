import { writable } from 'svelte/store';
// import io from "./socket.io.js";
import io from 'socket.io-client';

export const socket = writable(null);

export function initializeSocket() {
  console.log('Current url: ', window.location.href);
  let socketUrl = window.location.href;
  if(socketUrl.includes("5173/static")) {
    socketUrl = "http://localhost:8000";
  }
  const socketInstance = io(socketUrl);

  socketInstance.on('connect', () => {
    console.log('Socket connected');
    socket.set(socketInstance);
  });

  socketInstance.on('disconnect', () => {
    console.log('Socket disconnected');
    socket.set(null);
  });

  return socketInstance;
}
