const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const zoomInButton = document.getElementById("zoom-in");
const zoomOutButton = document.getElementById("zoom-out");
const zoomSlider = document.getElementById("zoom-slider");
const zoomLevel = document.getElementById("zoom-level");

// Set canvas size
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// SocketIO connection
const socket = io("http://localhost:8000");

let sprites = [];
let zoom = 1.0;
let panX = 0;
let panY = 0;
let isDragging = false;
let startX = 0;
let startY = 0;

// Render loop
function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(panX, panY);
    ctx.scale(zoom, zoom);

    ctx.fillStyle = "#006F05";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

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

socket.on("update_ui_state", (data) => {
    zoom = data.zoom;
    panX = data.pan_x;
    panY = data.pan_y;
    zoomSlider.value = zoom;
    zoomLevel.textContent = zoom.toFixed(1);
});

// UI event listeners
zoomInButton.addEventListener("click", () => {
    zoom = Math.min(zoom + 0.1, 3);
    socket.emit("update_ui_state", { zoom, pan_x: panX, pan_y: panY });
});

zoomOutButton.addEventListener("click", () => {
    zoom = Math.max(zoom - 0.1, 0.1);
    socket.emit("update_ui_state", { zoom, pan_x: panX, pan_y: panY });
});

zoomSlider.addEventListener("input", (e) => {
    zoom = parseFloat(e.target.value);
    socket.emit("update_ui_state", { zoom, pan_x: panX, pan_y: panY });
});

canvas.addEventListener('wheel', (e) => {
    console.log('scrolled');
    if (e.deltaY > 0) {
        zoom *= 1.03;
    } else {
        zoom /= 1.03;
    }
    socket.emit("update_ui_state", { zoom, pan_x: panX, pan_y: panY });
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
        // render();
    }
});

canvas.addEventListener('mouseup', () => {
    isDragging = false;
});

canvas.addEventListener('mouseleave', () => {
    isDragging = false;
});

// Start rendering
render();
