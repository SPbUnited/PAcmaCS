
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
    console.log("Field", field.width, field.height);
}
field.src = "field.svg";

var robot_yel = new Image();
robot_yel.onload = function() {
    console.log("Robot Yellow", robot_yel.width, robot_yel.height);
}
robot_yel.src = "robot_yel.svg";

var robot_blu = new Image();
robot_blu.onload = function() {
    console.log("Robot Blue", robot_blu.width, robot_blu.height);
}
robot_blu.src = "robot_blu.svg";

var ball = new Image();
ball.onload = function() {
    console.log("Ball", ball.width, ball.height);
}
ball.src = "ball.svg";

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

// https://stackoverflow.com/a/43155027
function drawRobot(image, x, y, rotation){
    cx = 90;
    cy = 90;
    scale = 1;
    ctx.save();
    ctx.translate(x, y); // sets scale and origin
    ctx.rotate(rotation);
    ctx.drawImage(image, -cx, -cy);
    ctx.restore();
}

function drawBall(x, y){
    ctx.drawImage(ball, x - ball.width/2, y - ball.height/2);
}

function drawSingleSprite(sprite){
    switch (sprite.type) {
        case "robot_yel":
            drawRobot(robot_yel, sprite.x, sprite.y, sprite.rotation);
            break;
        case "robot_blu":
            drawRobot(robot_blu, sprite.x, sprite.y, sprite.rotation);
            break;
        case "ball":
            drawBall(sprite.x, sprite.y);
            break;
        default:
            break;
    }
}

function drawSprites(sprites){
    sprites.forEach(sprite => {
        drawSingleSprite(sprite);
    });
}

// Render loop
function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(panX, panY);
    ctx.scale(zoom*zoom_param, zoom*zoom_param);

    // Draw field
    ctx.drawImage(field, -field.width/2, -field.height/2);

    // Render sprites
    drawSprites(sprites);

    ctx.restore();
    requestAnimationFrame(render);
}

// SocketIO events
socket.on("update_sprites", (data) => {
    sprites = data;
    console.log(sprites);
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
