const canvas_window = document.getElementById("canvas-window");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const zoomInButton = document.getElementById("zoom-in");
const zoomOutButton = document.getElementById("zoom-out");
const zoomSlider = document.getElementById("zoom-slider");
const zoomLevel = document.getElementById("zoom-level");
const resetButton = document.getElementById("reset");

// Set canvas size
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Load football field
var field = new Image();
field.onload = function() {
    ctx.drawImage(field, 0, 0);
    console.log(field.width, field.height);
}
field.src = "field.svg";

// SocketIO connection
const socket = io("http://localhost:8000");

// offsetHeight: 653
// \u200b
// offsetLeft: 0
// \u200b
// offsetParent: <div class="container">
// \u200b
// offsetTop: 0
// \u200b
// offsetWidth: 1415

let canvas_window_center_x = canvas_window.offsetTop + canvas_window.offsetWidth / 2;
let canvas_window_center_y = canvas_window.offsetLeft + canvas_window.offsetHeight / 2;

let sprites = [];
let zoom = 1;
const zoom_param = 0.25
let panX = canvas_window_center_x;
let panY = canvas_window_center_y;
let isDragging = false;
let startX = 0;
let startY = 0;

console.log(canvas_window)
// console.log(canvas_window.width, canvas_window.height);
console.log(canvas_window_center_x, canvas_window_center_y);
console.log(panX, panY);

// Render loop
function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(panX, panY);
    ctx.scale(zoom*zoom_param, zoom*zoom_param);

    ctx.drawImage(field, -field.width/2, -field.height/2);

    // ctx.fillStyle = "#006F05";
    // ctx.fillRect(0, 0, canvas.width, canvas.height);

    sprites.forEach(sprite => {
        const img = new Image();
        img.src = sprite.image;
        ctx.drawImage(img, sprite.x, sprite.y, 50, 50); // Adjust size as needed
    });

    ctx.restore();
    requestAnimationFrame(render);
}

// SocketIO events
socket.on("update_sprites", (data) => {
    sprites = data;
});

function update_ui_state()
{
    zoomSlider.value = zoom;
    zoomLevel.textContent = zoom.toFixed(1);
    socket.emit("updated_ui_state", {zoom, pan_x: panX, pan_y: panY});
    console.log("update_ui_state", zoom, panX, panY);
}

socket.on("update_ui_state", (data) => {
    zoom = data.zoom;
    panX = data.pan_x;
    panY = data.pan_y;
    update_ui_state();
});

// UI event listeners
zoomInButton.addEventListener("click", () => {
    zoom = Math.min(zoom + 0.1, 3);
    update_ui_state();
});

zoomOutButton.addEventListener("click", () => {
    zoom = Math.max(zoom - 0.1, 0.1);
    update_ui_state();
});

zoomSlider.addEventListener("input", (e) => {
    zoom = parseFloat(e.target.value);
    update_ui_state();
});

canvas.addEventListener('wheel', (e) => {
    console.log('scrolled');
    if (e.deltaY > 0) {
        zoom *= 1.03;
    } else {
        zoom /= 1.03;
    }
    zoom = Math.min(Math.max(zoom, 0.5), 3);
    update_ui_state();
});

resetButton.addEventListener("click", () => {
    zoom = 1;
    panX = canvas_window_center_x;
    panY = canvas_window_center_y;
    update_ui_state();
});

// Panning
canvas.addEventListener('mousedown', (e) => {
    isDragging = true;
    startX = e.clientX - panX;
    startY = e.clientY - panY;
});

canvas.addEventListener('mousemove', (e) => {
    if (isDragging) {
        panX = e.clientX - startX;
        panY = e.clientY - startY;
    }
    update_ui_state();
});

canvas.addEventListener('mouseup', () => {
    isDragging = false;
});

canvas.addEventListener('mouseleave', () => {
    isDragging = false;
});

// Start rendering
render();
