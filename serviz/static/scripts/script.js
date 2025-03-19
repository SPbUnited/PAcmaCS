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

var fields = {};
['divB', 'divC'].forEach(function (division) {
    var field = new Image();
    field.onload = function () {
        console.log("Field", field.width, field.height);
        fields[division] = field;
    }
    field.src = "/static/images/field_" + division + ".svg";
});
console.log(fields);

var yellow_robots = [];
// Load yellow robots
for (let i = 0; i < 16; i++) {
    yellow_robots[i] = new Image();
    yellow_robots[i].onload = function () {
        console.log("Robot Yellow", yellow_robots[i].width, yellow_robots[i].height);
    }
    yellow_robots[i].src = "/static/images/robots/y" + i + ".svg";
}

var yellow_robot_blank = new Image();
yellow_robot_blank.onload = function () {
    console.log("Robot Yellow Blank", yellow_robot_blank.width, yellow_robot_blank.height);
}
yellow_robot_blank.src = "/static/images/robot_yel.svg";

var blue_robots = [];
// Load blue robots
for (let i = 0; i < 16; i++) {
    blue_robots[i] = new Image();
    blue_robots[i].onload = function () {
        console.log("Robot Blue", blue_robots[i].width, blue_robots[i].height);
    }
    blue_robots[i].src = "/static/images/robots/b" + i + ".svg";
}

var blue_robot_blank = new Image();
blue_robot_blank.onload = function () {
    console.log("Robot blue Blank", blue_robot_blank.width, blue_robot_blank.height);
}
blue_robot_blank.src = "/static/images/robot_blu.svg";

var ball = new Image();
ball.onload = function () {
    console.log("Ball", ball.width, ball.height);
}
ball.src = "/static/images/ball.svg";

// SocketIO connection
const socket = io("http://localhost:8000");

let canvas_window_center_x = canvas_window.offsetTop + canvas_window.offsetWidth / 2;
let canvas_window_center_y = canvas_window.offsetLeft + canvas_window.offsetHeight / 2;

let currentDivision = 'divB';

let layer_data = [];
let zoom = 1;
const zoom_params = {
    'divB': 0.13,
    'divC': 0.25,
};
let zoom_param = zoom_params['divB'];
let panX = canvas_window_center_x;
let panY = canvas_window_center_y;
let isDragging = false;
let startX = 0;
let startY = 0;
let isBallDragging = false;
let startBallX = 0;
let startBallY = 0;
let deltaBallX = 0;
let deltaBallY = 0;
let velScaleFactor = 4;

console.log(canvas_window)
// console.log(canvas_window.width, canvas_window.height);
console.log(canvas_window_center_x, canvas_window_center_y);
console.log(panX, panY);

function drawField(division, field_orientation) {
    // console.log("Draw field", division, field_orientation);
    ctx.save();
    if (field_orientation == "left") {
        ctx.scale(-1, 1);
    }
    ctx.drawImage(fields[division], -fields[division].width / 2, -fields[division].height / 2);
    ctx.restore();
}

// https://stackoverflow.com/a/43155027
function drawRobot(team, robot_id, x, y, rotation, use_number_ids) {
    cx = 90;
    cy = 90;
    scale = 1;
    ctx.save();
    ctx.translate(x, y); // sets scale and origin
    ctx.rotate(-rotation);
    if (use_number_ids) {
        if (team == "y") {
            ctx.drawImage(yellow_robot_blank, -cx, -cy);
            ctx.fillStyle = "black";
        } else {
            ctx.drawImage(blue_robot_blank, -cx, -cy);
            ctx.fillStyle = "white";
        }
        ctx.rotate(rotation);
        ctx.font = "bold 100px Courier New";
        ctx.textAlign = "center";
        ctx.fillText(robot_id, 0, 40);
    }
    else {
        if (team == "y") {
            ctx.drawImage(yellow_robots[robot_id], -cx, -cy);
        } else {
            ctx.drawImage(blue_robots[robot_id], -cx, -cy);
        }
    }
    ctx.restore();
}

function drawBall(x, y) {
    ctx.drawImage(ball, x - ball.width / 2, y - ball.height / 2);
}

function drawSingleSprite(sprite, use_number_ids) {
    switch (sprite.type) {
        case "robot_yel":
            drawRobot("y", sprite.robot_id, sprite.x, -sprite.y, sprite.rotation, use_number_ids);
            break;
        case "robot_blu":
            drawRobot("b", sprite.robot_id, sprite.x, -sprite.y, sprite.rotation, use_number_ids);
            break;
        case "ball":
            drawBall(sprite.x, -sprite.y);
            break;
        default:
            break;
    }
}

function drawLayer(layer, use_number_ids) {
    layer.forEach(sprite => {
        // console.log(sprite)
        drawSingleSprite(sprite, use_number_ids);
    });
}

function toggleLayerVisibilityByIndex(layer_index) {
    layer_index -= 1;
    if (layer_index >= 0 && layer_index < Object.keys(layer_data).length) {
        layer_name = Object.keys(layer_data)[layer_index];
        toggleLayerVisibility(layer_name);
    }
}

function toggleLayerVisibility(layer_name) {
    console.info("Toggle layer visibility", layer_name);
    socket.emit("toggle_layer_visibility", layer_name);
}

function layerDivGenerator(layers, layer_name, layer_data) {
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

function iterateLayers(layers, use_number_ids) {
    layerList.innerHTML = "";
    for (const [layer_name, layer_data] of Object.entries(layers)) {
        // console.log(layer_name, layer_data);
        layerList.appendChild(layerDivGenerator(layers, layer_name, layer_data));

        if (!layer_data["is_visible"]) {
            continue;
        }

        drawLayer(layer_data["data"], use_number_ids);
    }
}

function drawArrow(x, y, angle, length) {
    ctx.beginPath();
    ctx.lineCap = "round";

    ctx.moveTo(x, y);
    ctx.lineTo(x + Math.cos(angle) * length, y + Math.sin(angle) * length);

    const tipX = x + Math.cos(angle) * length;
    const tipY = y + Math.sin(angle) * length;

    const arrowFactor = 40;
    // Arrowhead
    ctx.moveTo(tipX, tipY);
    ctx.lineTo(
        tipX - Math.cos(angle - Math.PI/6) * arrowFactor,
        tipY - Math.sin(angle - Math.PI/6) * arrowFactor
    );
    ctx.moveTo(tipX, tipY);
    ctx.lineTo(
        tipX - Math.cos(angle + Math.PI/6) * arrowFactor,
        tipY - Math.sin(angle + Math.PI/6) * arrowFactor
    );

    // ctx.strokeStyle = "#ff0000";
    ctx.strokeStyle = "#E8D743";
    ctx.lineWidth = 10;
    ctx.stroke();
}

// Render loop
function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(panX, panY);
    ctx.scale(zoom * zoom_param, zoom * zoom_param);

    // Draw field
    field_orientation = document.getElementById("field-orientation").checked ? "left" : "right";
    drawField(currentDivision, field_orientation);

    // Render sprites
    use_number_ids = document.getElementById("use-number-ids").checked;
    iterateLayers(layer_data, use_number_ids);

    if (isBallDragging) {
        const ballVel = Math.sqrt(Math.pow(deltaBallX, 2) + Math.pow(deltaBallY, 2));
        drawArrow(startBallX, startBallY, Math.atan2(deltaBallY, deltaBallX), ballVel);
    }


    ctx.restore();
    requestAnimationFrame(render);
}

// SocketIO events
socket.on("update_division", (data) => {
    currentDivision = data;
    zoom_param = zoom_params[currentDivision];
    console.log("Update division", data);
});

socket.on("update_sprites", (data) => {
    layer_data = data;
    // console.log(layer_data);
});

function update_ui_state() {
    zoomSlider.value = zoom;
    zoomLevel.textContent = zoom.toFixed(1);
    socket.emit("updated_ui_state", { zoom, pan_x: panX, pan_y: panY });
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

    if(e.altKey) {
        isBallDragging = true;
    }
    startBallX = startX / (zoom * zoom_param);
    startBallY = startY / (zoom * zoom_param);
    deltaBallX = 0;
    deltaBallY = 0;
});

canvas.addEventListener('mousemove', (e) => {
    if (!isDragging) {
        return;
    }

    if (e.altKey) {
        deltaBallX = - ((e.clientX - panX) / (zoom * zoom_param) - startBallX);
        deltaBallY = - ((e.clientY - panY) / (zoom * zoom_param) - startBallY);
        console.log(deltaBallX, deltaBallY);
    }
    else {
        panX = e.clientX - startX;
        panY = e.clientY - startY;
        update_ui_state();
    }
});

canvas.addEventListener('mouseup', (e) => {
    if (isDragging && e.altKey) {
        const vx = deltaBallX * velScaleFactor;
        const vy = deltaBallY * velScaleFactor;
        socket.emit("send_signal", { "larcmacs": "set_ball", "data": { "x": startBallX, "y": -startBallY, "vx": vx, "vy": -vy } });
    }
    isDragging = false;
    isBallDragging = false;
});

canvas.addEventListener('mouseleave', () => {
    isDragging = false;
    isBallDragging = false;
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

        // Display parameters
        case 'f':
            document.getElementById("field-orientation").click();
            break;
        case 'i':
            document.getElementById("use-number-ids").click();
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
window.addEventListener('load', function () {
    render();
})