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
    ctx.translate(x, y);
    ctx.rotate(rotation);
    if (use_number_ids) {
        if (team === "y") {
            ctx.drawImage(yellow_robot_blank, -cx, -cy);
            ctx.fillStyle = "black";
        } else {
            ctx.drawImage(blue_robot_blank, -cx, -cy);
            ctx.fillStyle = "white";
        }
        ctx.rotate(-rotation);
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
    ctx.drawImage(ball, x - ball.width / 2, y - ball.height / 2);
}

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
        default:
            break;
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

export function drawArrow(ctx, x, y, angle, length) {
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

