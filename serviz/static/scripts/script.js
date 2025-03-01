const canvas_window = document.getElementById("canvas-window");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const zoomInButton = document.getElementById("zoom-in");
const zoomOutButton = document.getElementById("zoom-out");
const zoomSlider = document.getElementById("zoom-slider");
const zoomLevel = document.getElementById("zoom-level");
const resetButton = document.getElementById("reset");
const testButton = document.getElementById("test_button");
const layerList = document.getElementById("layer-list");

// Set canvas size
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Load football field
var field = new Image();
field.onload = function() {
    console.log("Field", field.width, field.height);
}
field.src = "/static/images/field.svg";

var yellow_robots = [];
// Load yellow robots
for (let i = 0; i < 16; i++) {
    yellow_robots[i] = new Image();
    yellow_robots[i].onload = function() {
        console.log("Robot Yellow", yellow_robots[i].width, yellow_robots[i].height);
    }
    yellow_robots[i].src = "/static/images/robots/y" + i + ".svg";
}

var blue_robots = [];
// Load blue robots
for (let i = 0; i < 16; i++) {
    blue_robots[i] = new Image();
    blue_robots[i].onload = function() {
        console.log("Robot Blue", blue_robots[i].width, blue_robots[i].height);
    }
    blue_robots[i].src = "/static/images/robots/b" + i + ".svg";
}

var ball = new Image();
ball.onload = function() {
    console.log("Ball", ball.width, ball.height);
}
ball.src = "/static/images/ball.svg";

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

let layer_data = [];
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

function drawField(field_orientation){
    console.log("Draw field", field_orientation);
    ctx.save();
    if (field_orientation == "left") {
        ctx.scale(-1, 1);
    }
    ctx.drawImage(field, -field.width/2, -field.height/2);
    ctx.restore();
}

// https://stackoverflow.com/a/43155027
function drawRobot(team, robot_id, x, y, rotation){
    cx = 90;
    cy = 90;
    scale = 1;
    ctx.save();
    ctx.translate(x, y); // sets scale and origin
    ctx.rotate(rotation);
    if(team == "y") {
        ctx.drawImage(yellow_robots[robot_id], -cx, -cy);
    } else {
        ctx.drawImage(blue_robots[robot_id], -cx, -cy);
    }
    ctx.restore();
}

function drawBall(x, y){
    ctx.drawImage(ball, x - ball.width/2, y - ball.height/2);
}

function drawSingleSprite(sprite){
    switch (sprite.type) {
        case "robot_yel":
            drawRobot("y", sprite.robot_id, sprite.x, sprite.y, sprite.rotation);
            break;
        case "robot_blu":
            drawRobot("b", sprite.robot_id, sprite.x, sprite.y, sprite.rotation);
            break;
        case "ball":
            drawBall(sprite.x, sprite.y);
            break;
        default:
            break;
    }
}

function drawLayer(layer){
    layer.forEach(sprite => {
        console.log(sprite)
        drawSingleSprite(sprite);
    });
}

function toggleLayerVisibilityByIndex(layer_index){
    layer_index -= 1;
    if (layer_index >= 0 && layer_index < Object.keys(layer_data).length) {
        layer_name = Object.keys(layer_data)[layer_index];
        toggleLayerVisibility(layer_name);
    }
}

function toggleLayerVisibility(layer_name){
    console.info("Toggle layer visibility", layer_name);
    socket.emit("toggle_layer_visibility", layer_name);
}

function layerDivGenerator(layers, layer_name, layer_data){
    const layerItem = document.createElement("div");
    layerItem.className = "layer-item";

    const index = Object.keys(layers).indexOf(layer_name);
    const layerIndex = "<tt>[" + (index + 1) + "]</tt>";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.id = `layer-${layer_name}`;
    checkbox.checked = layer_data["is_visible"];

    const label = document.createElement("label");
    label.htmlFor = `layer-${layer_name}`;
    label.textContent = layer_name;

    layerItem.addEventListener("mousedown", () => toggleLayerVisibility(layer_name));
    layerItem.innerHTML += layerIndex;
    // layerItem.appendChild(layerIndex);
    layerItem.appendChild(checkbox);
    layerItem.appendChild(label);
    return layerItem
}

function iterateLayers(layers){
    layerList.innerHTML = "";
    for (const [layer_name, layer_data] of Object.entries(layers)) {
        console.log(layer_name, layer_data);
        layerList.appendChild(layerDivGenerator(layers, layer_name, layer_data));

        if (!layer_data["is_visible"]) {
            continue;
        }

        drawLayer(layer_data["data"]);
    }
}

// Render loop
function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(panX, panY);
    ctx.scale(zoom*zoom_param, zoom*zoom_param);

    // Draw field
    field_orientation = document.getElementById("field-orientation").checked ? "left" : "right";
    drawField(field_orientation);

    // Render sprites
    iterateLayers(layer_data);

    ctx.restore();
    requestAnimationFrame(render);
}

// SocketIO events
socket.on("update_sprites", (data) => {
    layer_data = data;
    // console.log(layer_data);
});

function update_ui_state()
{
    zoomSlider.value = zoom;
    zoomLevel.textContent = zoom.toFixed(1);
    socket.emit("updated_ui_state", {zoom, pan_x: panX, pan_y: panY});
    // console.log("update_ui_state", zoom, panX, panY);
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
    // console.log('scrolled');
    if (e.deltaY > 0) {
        zoom *= 1.03;
    } else {
        zoom /= 1.03;
    }
    zoom = Math.min(Math.max(zoom, 0.5), 3);
    update_ui_state();
});

window.addEventListener("resize", () => {
    canvas_window_center_x = canvas_window.offsetTop + canvas_window.offsetWidth / 2;
    canvas_window_center_y = canvas_window.offsetLeft + canvas_window.offsetHeight / 2;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    update_ui_state();
});

resetButton.addEventListener("click", () => {
    zoom = 1;
    panX = canvas_window_center_x;
    panY = canvas_window_center_y;
    update_ui_state();
});

testButton.addEventListener("click", () => {
    // console.log("test");
    socket.emit("test_signal", {});
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
        update_ui_state();
    }
});

canvas.addEventListener('mouseup', () => {
    isDragging = false;
});

canvas.addEventListener('mouseleave', () => {
    isDragging = false;
});

// Keyboard hotkeys
window.addEventListener('keydown', (e) => {
    let panAmount = 100;
    switch (e.key) {
        // Movement
        case 'r':
            resetButton.click();
            break;
        case 'ArrowUp':
        case 'k':
            panY += panAmount;
            break;
        case 'ArrowDown':
        case 'j':
            panY -= panAmount;
            break;
        case 'ArrowLeft':
        case 'h':
            panX += panAmount;
            break;
        case 'ArrowRight':
        case 'l':
            panX -= panAmount;
            break;
        // Zoom
        case '-':
            zoomOutButton.click();
            break;
        case '=':
            zoomInButton.click();
            break;

        // Field orientation
        case 'f':
            document.getElementById("field-orientation").click();
            break;

        // Control
        case 't':
            testButton.click();
            break;

        case '1':
        case '2':
        case '3':
        case '4':
        case '5':
        case '6':
        case '7':
        case '8':
        case '9':
            toggleLayerVisibilityByIndex(e.key);
            break;

        default:
            break;
    }
    update_ui_state();
});

// Start rendering
render();
