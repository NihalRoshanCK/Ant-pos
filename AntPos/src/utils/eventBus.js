import { reactive } from 'vue';

const eventBus = reactive({});

// Function to emit an event
eventBus.emit = function(event, ...args) {
  if (!this[event]) return;
  this[event].forEach(fn => fn(...args));
};

// Function to listen for an event
eventBus.on = function(event, fn) {
  if (!this[event]) {
    this[event] = [];
  }
  this[event].push(fn);
};

// Function to remove an event listener
eventBus.off = function(event, fn) {
  if (!this[event]) return;
  this[event] = this[event].filter(listener => listener !== fn);
};

export default eventBus;