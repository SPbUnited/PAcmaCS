// drawing.js

// Ensure these variables are globally available in your project
// (or pass them as parameters to a class/function if preferred)
// const ctx = canvas.getContext("2d");
// const layerList = document.getElementById("layer-list");
// const fields = [...];
// const yellow_robot_blank = ...;


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

function drawRobot(ctx, team, robot_id, x, y, rotation, use_number_ids) {
    const cx = 90;
    const cy = 90;
    ctx.save();
    ctx.translate(Math.floor(x), Math.floor(y));
    ctx.rotate(-rotation);
    if (use_number_ids) {
        if (team === "y") {
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
    } else {
        if (team === "y") {
            ctx.drawImage(yellow_robots[robot_id], -cx, -cy);
        } else {
            ctx.drawImage(blue_robots[robot_id], -cx, -cy);
        }
    }
    ctx.restore();
}

function drawBall(ctx, x, y) {
    ctx.drawImage(ball, Math.floor(x - ball.width / 2), Math.floor(y - ball.height / 2));
}

function drawLine(ctx, x_list, y_list, color, width) {
    let x = x_list[0];
    let y = -y_list[0];
    ctx.beginPath();
    ctx.moveTo(x, y);

    for (let i = 1; i < x_list.length; i++) {
        x = x_list[i];
        y = -y_list[i];
        ctx.lineTo(x, y);
    }

    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.stroke();
}

function drawPolygon(ctx, x_list, y_list, color, width) {
    let x = x_list[0];
    let y = -y_list[0];
    ctx.beginPath();
    ctx.moveTo(x, y);

    for (let i = 1; i < x_list.length; i++) {
        x = x_list[i];
        y = -y_list[i];
        ctx.lineTo(x, y);
    }

    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();

    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.stroke();
}

function drawRect(ctx, x, y, width, height, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x, y, width, height);
}

function drawCircle(ctx, x, y, radius, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, 2 * Math.PI);
    ctx.fill();
}

function drawText(ctx, text, x, y, color = "black", modifiers = "42px", align = "left")
{
    ctx.font = modifiers + " Courier New";
    ctx.fillStyle = color;
    ctx.textAlign = align;
    ctx.fillText(text, x, y);
}

/**
 * Drawing API Reference
 *
 * sprite.type
 * - robot_yel
 * - robot_blu
 * - ball
 * - line
 * - polygon
 * - rect
 *
 * expected fields:
 * # robot_yel
 *      - robot_id
 *      - x
 *      - y
 *      - rotation
 *      -* vx
 *      -* vy
 * # robot_blu
 *      - robot_id
 *      - x
 *      - y
 *      - rotation
 *      -* vx
 *      -* vy
 *
 * # ball
 *      - x
 *      - y
 *      -* vx
 *      -* vy
 *
 * # line
 *      - x_list
 *      - y_list
 *      - color
 *      - width
 *
 * # arrow
 *      - x
 *      - y
 *      - dx
 *      - dy
 *      - color
 *      - width
 *
 * # polygon
 *      - x_list
 *      - y_list
 *      - color
 *      - width
 *
 * # rect
 *      - x
 *      - y
 *      - width
 *      - height
 *      - color
 *
 * # circle
 *      - x
 *      - y
 *      - radius
 *      - color
 * # text
 *      - text
 *      - x
 *      - y
 *      - color [black, white, etc.]
 *      - modifiers [bold, italic, etc., size: 42px, 100px, etc.]
 *      - align [left, center, right]
 */
function drawSingleSprite(ctx, sprite, use_number_ids) {
    switch (sprite.type) {
        case "robot_yel":
            drawRobot(ctx, "y", sprite.robot_id, sprite.x, -sprite.y, sprite.rotation, use_number_ids);
            break;
        case "robot_blu":
            drawRobot(ctx, "b", sprite.robot_id, sprite.x, -sprite.y, sprite.rotation, use_number_ids);
            break;
        case "ball":
            drawBall(ctx, sprite.x, -sprite.y);
            break;
        case "line":
            drawLine(ctx, sprite.x_list, sprite.y_list, sprite.color, sprite.width);
            break;
        case "arrow":
            drawArrow(ctx, sprite.x, -sprite.y, sprite.dx, -sprite.dy, sprite.color, sprite.width);
            break;
        case "polygon":
            drawPolygon(ctx, sprite.x_list, sprite.y_list, sprite.color, sprite.width);
            break;
        case "rect":
            drawRect(ctx, sprite.x, -sprite.y, sprite.width, -sprite.height, sprite.color);
            break;
        case "circle":
            drawCircle(ctx, sprite.x, -sprite.y, sprite.radius, sprite.color);
            break;
        case "text":
            drawText(ctx, sprite.text, sprite.x, -sprite.y, sprite.color, sprite.modifiers, sprite.align);
            break;
        default:
            break;
    }
    if (sprite.vx !== undefined && sprite.vy !== undefined) {
        const k = 1;
        const threshold = 10;
        if(Math.abs(sprite.vx) > threshold && Math.abs(sprite.vy) > threshold)
        {
            console.log(sprite.vx, sprite.vy);
            drawArrow(ctx,
                sprite.x,
                -sprite.y,
                sprite.vx * k,
                -sprite.vy * k);
        }
    }
}

function drawLayer(ctx, layer, use_number_ids) {
    layer.forEach(sprite => {
        drawSingleSprite(ctx, sprite, use_number_ids);
    });
}

// Export only iterateLayers
export function iterateLayers(ctx, layers, use_number_ids) {
    // layerList.innerHTML = "";
    for (const [layer_name, layer_data] of Object.entries(layers)) {
        // layerList.appendChild(layerDivGenerator(layers, layer_name, layer_data));
        if (!layer_data.is_visible) continue;
        drawLayer(ctx, layer_data.data, use_number_ids);
    }
}

export function drawArrow(ctx, x, y, dx, dy, color = "#E8D743", width = 10) {
    ctx.beginPath();
    ctx.lineCap = "round";

    ctx.moveTo(x, y);
    ctx.lineTo(x + dx, y + dy);

    const tipX = x + dx;
    const tipY = y + dy;

    const arrowFactor = 4 * width;
    // Arrowhead
    const angle = Math.atan2(dy, dx);
    ctx.moveTo(tipX, tipY);
    ctx.lineTo(
        tipX - Math.cos(angle - Math.PI / 6) * arrowFactor,
        tipY - Math.sin(angle - Math.PI / 6) * arrowFactor
    );
    ctx.moveTo(tipX, tipY);
    ctx.lineTo(
        tipX - Math.cos(angle + Math.PI / 6) * arrowFactor,
        tipY - Math.sin(angle + Math.PI / 6) * arrowFactor
    );

    // ctx.strokeStyle = "#ff0000";
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.stroke();
}

