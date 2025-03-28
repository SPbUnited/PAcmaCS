import { writable } from 'svelte/store';
// import io from "./socket.io.js";
import io from 'socket.io-client';

export const socket = writable(null);

export function initializeSocket() {
  const socketInstance = io('http://localhost:8000');

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
