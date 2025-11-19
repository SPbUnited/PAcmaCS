import Component from "../loadComponents";
import { bus, subscribeToTopic, sendMessage } from "../socketManager";

const Field: Component = {
  name: "Field",
  factory: (container) => {
    container.element.style.position = "relative";

    let fieldConfig = defaultFieldCfg;

    // Create field svg
    const svgNS = "http://www.w3.org/2000/svg";
    const fieldSvg = document.createElementNS(svgNS, "svg");
    fieldSvg.style.position = "absolute";
    fieldSvg.style.top = "0";
    fieldSvg.style.left = "0";
    fieldSvg.setAttribute("preserveAspectRatio", "xMidYMid meet");
    fieldSvg.style.display = "block";
    fieldSvg.style.userSelect = "none";
    fieldSvg.style.touchAction = "none";
    container.element.append(fieldSvg);

    const textSvg = document.createElementNS(svgNS, "svg");
    textSvg.style.position = "absolute";
    textSvg.style.top = "0";
    textSvg.style.left = "0";
    textSvg.setAttribute("preserveAspectRatio", "xMidYMid meet");
    textSvg.style.display = "block";
    textSvg.style.userSelect = "none";
    textSvg.style.touchAction = "none";
    textSvg.style.pointerEvents = "none";
    container.element.append(textSvg);

    const drawingSvg = document.createElementNS(svgNS, "svg");
    drawingSvg.style.position = "absolute";
    drawingSvg.style.top = "0";
    drawingSvg.style.left = "0";
    drawingSvg.setAttribute("preserveAspectRatio", "xMidYMid meet");
    drawingSvg.style.display = "block";
    drawingSvg.style.userSelect = "none";
    drawingSvg.style.touchAction = "none";
    drawingSvg.style.pointerEvents = "none";
    container.element.append(drawingSvg);

    // Create display with coords
    const coordsDisplay = document.createElement("div");
    coordsDisplay.style.position = "absolute";
    coordsDisplay.style.bottom = "0";
    coordsDisplay.style.left = "0";
    coordsDisplay.style.background = "rgba(0, 0, 0, 0.6)";
    coordsDisplay.style.color = "white";
    coordsDisplay.style.fontFamily = "monospace";
    coordsDisplay.style.fontSize = "13px";
    coordsDisplay.style.pointerEvents = "none";
    container.element.append(coordsDisplay);

    // Field image initial config
    let scale = 0.9;
    let originX = 0;
    let originY = 0;

    let isDrawingArrow = false;
    let draggingArrowX = 0;
    let draggingArrowY = 0;
    let isDragging = false;
    let dragStartX = 0;
    let dragStartY = 0;

    // Settings of display with coords

    fieldSvg.addEventListener("mousemove", (e) => {
      const pt = fieldSvg.createSVGPoint();
      pt.x = e.clientX;
      pt.y = e.clientY;
      const svgP = pt.matrixTransform(fieldSvg.getScreenCTM()?.inverse());

      coordsDisplay.textContent = `X: ${svgP.x.toFixed(
        0
      )}, Y: ${-svgP.y.toFixed(0)}`;
    });
    fieldSvg.addEventListener("mouseleave", (e) => {
      coordsDisplay.textContent = ``;
    });

    // Settings of field image
    function updateTransform() {
      fieldSvg.style.transform = `translate(${originX}px, ${originY}px) scale(${scale})`;
      drawingSvg.style.transform = fieldSvg.style.transform;
      textSvg.style.transform = fieldSvg.style.transform;
    }
    container.element.addEventListener(
      "wheel",
      (e) => {
        e.preventDefault();

        const rect = fieldSvg.getBoundingClientRect();

        const scaleFactor = e.deltaY > 0 ? 1 / 1.1 : 1.1;
        const newScale = scale * scaleFactor;
        if (newScale > 0.3 && newScale < 10) {
          originX +=
            (e.clientX - (rect.left + rect.right) / 2) * (1 - scaleFactor);
          originY +=
            (e.clientY - (rect.top + rect.bottom) / 2) * (1 - scaleFactor);

          scale = newScale;
          updateTransform();
        }
      },
      { passive: false }
    );
    container.element.addEventListener("mousedown", (e) => {
      if (e.altKey) {
        isDrawingArrow = true;
        const pt = fieldSvg.createSVGPoint();
        pt.x = e.clientX;
        pt.y = e.clientY;
        const svgP = pt.matrixTransform(fieldSvg.getScreenCTM()?.inverse());
        dragStartX = svgP.x;
        dragStartY = svgP.y;
        draggingArrowX = dragStartX;
        draggingArrowY = dragStartY;
      } else {
        dragStartX = e.clientX - originX;
        dragStartY = e.clientY - originY;
      }
      isDragging = true;
    });
    window.addEventListener("mouseup", () => {
      isDragging = false;
      isDrawingArrow = false;
      finishArrow();
    });
    window.addEventListener("mousemove", (e) => {
      if (!isDragging) return;
      if (isDrawingArrow) {
        const pt = fieldSvg.createSVGPoint();
        pt.x = e.clientX;
        pt.y = e.clientY;
        const svgP = pt.matrixTransform(fieldSvg.getScreenCTM()?.inverse());
        draggingArrowX = svgP.x;
        draggingArrowY = svgP.y;
      } else {
        originX = e.clientX - dragStartX;
        originY = e.clientY - dragStartY;
        updateTransform();
      }
    });

    subscribeToTopic("update_geometry");
    bus.on("update_geometry", (data) => {
      // console.log("Update field with new data:", data);
      fieldConfig = {
        width: data.length,
        height: data.width,
        leftGoalColor: "#FFFF00",
        rightGoalColor: "#0000FF",
        goalWidth: data.goalWidth,
        goalDepth: data.goalDepth,
        penaltyAreaWidth: data.penaltyAreaWidth,
        penaltyAreaDepth: data.penaltyAreaDepth,
        centerCircleRadius: data.centerCircleRadius,
        borderSize: data.borderSize,
      };
      drawField(fieldSvg, fieldConfig);
      updateViewBox([drawingSvg, fieldSvg, textSvg], fieldConfig);
      updateTransform();
    });

    let lastSprites: any = null;
    let isDrawing = false;
    subscribeToTopic("update_sprites");
    bus.on("update_sprites", (data) => {
      lastSprites = data;
      requestDraw();

      if ("_time_from_update" in data) {
        const time_from_update = data["_time_from_update"];
        if (time_from_update < 1) {
          textSvg.innerHTML = "";
        } else if (textSvg.innerHTML == "") {
          const text = document.createElementNS(svgNS, "text");
          text.setAttribute("x", "0");
          text.setAttribute("y", "0");
          text.setAttribute("fill", "#88dd00");
          text.setAttribute("font-size", "1000");
          text.setAttribute("text-anchor", "middle");
          text.setAttribute("dominant-baseline", "middle");
          text.setAttribute("dy", "0.1em");
          text.textContent = "NO DATA";
          textSvg.appendChild(text);
        }
      }
    });
    function requestDraw() {
      if (isDrawing) return;
      isDrawing = true;

      requestAnimationFrame(() => {
        if (lastSprites) {
          drawImageSvg(drawingSvg, lastSprites);
          if (isDrawingArrow) {
            updateArrow(
              drawingSvg,
              dragStartX,
              dragStartY,
              draggingArrowX,
              draggingArrowY
            );
          }
          lastSprites = null;
        }
        isDrawing = false;
      });
    }

    drawField(fieldSvg, fieldConfig);
    updateViewBox([drawingSvg, fieldSvg, textSvg], fieldConfig);
    requestAnimationFrame(() => {
      const windowRect = container.element.getBoundingClientRect();
      const fieldRect = fieldSvg.getBoundingClientRect();
      originX = (windowRect.width - fieldRect.width) / 2;
      originY = (windowRect.height - fieldRect.height) / 2;
      updateTransform();
    });

    let arrowLine: SVGLineElement | null = null;

    function updateArrow(
      svg: SVGSVGElement,
      x1: number,
      y1: number,
      x2: number,
      y2: number
    ) {
      const color = "#ffb325";
      const markerId = `arrow-${color.replace("#", "")}`;
      createArrowMarker(svg, color, markerId);

      arrowLine = document.createElementNS(svgNS, "line");
      arrowLine.setAttribute("x1", x1.toString());
      arrowLine.setAttribute("y1", y1.toString());
      arrowLine.setAttribute("x2", (x1 * 2 - x2).toString());
      arrowLine.setAttribute("y2", (y1 * 2 - y2).toString());
      arrowLine.setAttribute("stroke", color);
      arrowLine.setAttribute("stroke-width", "20");
      arrowLine.setAttribute("marker-end", `url(#${markerId})`);
      svg.appendChild(arrowLine);

      const speed = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
      if (speed > 100) {
        const deltaY = y2 < y1 ? -100 : 100;

        const text = document.createElementNS(svgNS, "text");
        text.textContent = `${(speed / 1000).toFixed(1)} m/s`;
        text.setAttribute("x", x1.toString());
        text.setAttribute("y", (y1 + deltaY).toString());
        text.setAttribute("fill", color);
        text.setAttribute("font-size", "200");
        text.setAttribute("font-weight", "bold");
        text.setAttribute("text-anchor", "middle");
        text.setAttribute("dominant-baseline", "middle");
        svg.appendChild(text);
      }
    }

    function finishArrow() {
      if (!arrowLine) return;

      const x = dragStartX;
      const y = dragStartY;
      const vx = dragStartX - draggingArrowX;
      const vy = dragStartY - draggingArrowY;
      sendMessage("send_signal", {
        transnet: "set_ball",
        data: { x: x, y: -y, vx: vx, vy: -vy },
      });
      console.log(vx, vy);

      arrowLine = null;
    }
  },
};

export default Field;

interface FieldConfig {
  width: number;
  height: number;
  leftGoalColor: string;
  rightGoalColor: string;
  goalWidth: number;
  goalDepth: number;
  penaltyAreaWidth: number;
  penaltyAreaDepth: number;
  centerCircleRadius: number;
  borderSize: number;
}

const defaultFieldCfg: FieldConfig = {
  width: 9000,
  height: 6000,
  leftGoalColor: "#0000ff",
  rightGoalColor: "#ffff00",
  goalWidth: 1000,
  goalDepth: 180,
  penaltyAreaWidth: 2000,
  penaltyAreaDepth: 1000,
  centerCircleRadius: 500,
  borderSize: 250,
};

function drawField(fieldSvg: SVGSVGElement, cfg: FieldConfig): void {
  const fieldColor = "#27bb27";
  const lineWidth = "10";
  const goalLineWidth = 40;

  fieldSvg.innerHTML = "";

  const svgNS = "http://www.w3.org/2000/svg";

  fieldSvg.setAttribute(
    "viewBox",
    `${-cfg.width / 2 - cfg.borderSize} ${-cfg.height / 2 - cfg.borderSize} ${
      cfg.width + cfg.borderSize * 2
    } ${cfg.height + cfg.borderSize * 2}`
  );
  fieldSvg.setAttribute("preserveAspectRatio", "xMidYMid meet");

  const field = document.createElementNS(svgNS, "rect");
  field.setAttribute("x", String(-cfg.width / 2 - cfg.borderSize));
  field.setAttribute("y", String(-cfg.height / 2 - cfg.borderSize));
  field.setAttribute("width", String(cfg.width + cfg.borderSize * 2));
  field.setAttribute("height", String(cfg.height + cfg.borderSize * 2));
  field.setAttribute("fill", fieldColor);
  fieldSvg.appendChild(field);

  const boarder_rect = document.createElementNS(svgNS, "rect");
  boarder_rect.setAttribute("x", String(-cfg.width / 2));
  boarder_rect.setAttribute("y", String(-cfg.height / 2));
  boarder_rect.setAttribute("width", String(cfg.width));
  boarder_rect.setAttribute("height", String(cfg.height));
  boarder_rect.setAttribute("fill", fieldColor);
  boarder_rect.setAttribute("stroke", "white");
  boarder_rect.setAttribute("stroke-width", lineWidth);
  fieldSvg.appendChild(boarder_rect);

  const circle = document.createElementNS(svgNS, "circle");
  circle.setAttribute("r", String(cfg.centerCircleRadius));
  circle.setAttribute("fill", fieldColor);
  circle.setAttribute("stroke", "white");
  circle.setAttribute("stroke-width", lineWidth);
  fieldSvg.appendChild(circle);

  const center = document.createElementNS(svgNS, "circle");
  center.setAttribute("r", "25");
  center.setAttribute("fill", "white");
  fieldSvg.appendChild(center);

  const halfLine = document.createElementNS(svgNS, "line");
  halfLine.setAttribute("y1", String(-cfg.height / 2));
  halfLine.setAttribute("y2", String(cfg.height / 2));
  halfLine.setAttribute("stroke", "white");
  halfLine.setAttribute("stroke-width", lineWidth);
  fieldSvg.appendChild(halfLine);

  const leftGoal = document.createElementNS(svgNS, "rect");
  leftGoal.setAttribute(
    "x",
    String(-(cfg.width / 2 + cfg.goalDepth - goalLineWidth / 2))
  );
  leftGoal.setAttribute("y", String(-cfg.goalWidth / 2));
  leftGoal.setAttribute("width", String(cfg.goalDepth));
  leftGoal.setAttribute("height", String(cfg.goalWidth));
  leftGoal.setAttribute("fill", fieldColor);
  leftGoal.setAttribute("stroke", cfg.leftGoalColor);
  leftGoal.setAttribute("stroke-width", String(goalLineWidth));
  fieldSvg.appendChild(leftGoal);

  const leftPenalty = document.createElementNS(svgNS, "rect");
  leftPenalty.setAttribute("x", String(-cfg.width / 2));
  leftPenalty.setAttribute("y", String(-cfg.penaltyAreaWidth / 2));
  leftPenalty.setAttribute("width", String(cfg.penaltyAreaDepth));
  leftPenalty.setAttribute("height", String(cfg.penaltyAreaWidth));
  leftPenalty.setAttribute("fill", fieldColor);
  leftPenalty.setAttribute("stroke", "white");
  leftPenalty.setAttribute("stroke-width", lineWidth);
  fieldSvg.appendChild(leftPenalty);

  const rightGoal = document.createElementNS(svgNS, "rect");
  rightGoal.setAttribute("x", String(cfg.width / 2 - goalLineWidth / 2));
  rightGoal.setAttribute("y", String(-cfg.goalWidth / 2));
  rightGoal.setAttribute("width", String(cfg.goalDepth));
  rightGoal.setAttribute("height", String(cfg.goalWidth));
  rightGoal.setAttribute("fill", fieldColor);
  rightGoal.setAttribute("stroke", cfg.rightGoalColor);
  rightGoal.setAttribute("stroke-width", "50");
  fieldSvg.appendChild(rightGoal);

  const rightPenalty = document.createElementNS(svgNS, "rect");
  rightPenalty.setAttribute("x", String(cfg.width / 2 - cfg.penaltyAreaDepth));
  rightPenalty.setAttribute("y", String(-cfg.penaltyAreaWidth / 2));
  rightPenalty.setAttribute("width", String(cfg.penaltyAreaDepth));
  rightPenalty.setAttribute("height", String(cfg.penaltyAreaWidth));
  rightPenalty.setAttribute("fill", fieldColor);
  rightPenalty.setAttribute("stroke", "white");
  rightPenalty.setAttribute("stroke-width", lineWidth);
  fieldSvg.appendChild(rightPenalty);

  const goalLine = document.createElementNS(svgNS, "line");
  goalLine.setAttribute("x1", String(-cfg.width / 2));
  goalLine.setAttribute("x2", String(cfg.width / 2));
  goalLine.setAttribute("stroke", "white");
  goalLine.setAttribute("stroke-width", lineWidth);
  fieldSvg.appendChild(goalLine);
}

function updateViewBox(Svgs: SVGSVGElement[], cfg: FieldConfig) {
  const x = -cfg.width / 2 - cfg.borderSize;
  const y = -cfg.height / 2 - cfg.borderSize;
  const w = cfg.width + cfg.borderSize * 2;
  const h = cfg.height + cfg.borderSize * 2;
  Svgs.forEach((SVG) => {
    SVG.setAttribute("viewBox", `${x} ${y} ${w} ${h}`);
  });
}

interface RobotBase {
  x: number;
  y: number;
  rotation?: number;
  vx?: number;
  vy?: number;
  robot_id: number;
}

interface RobotYel extends RobotBase {
  type: "robot_yel";
}

interface RobotBlu extends RobotBase {
  type: "robot_blu";
}

interface Ball {
  type: "ball";
  x: number;
  y: number;
  vx?: number;
  vy?: number;
}

interface Line {
  type: "line";
  x_list: number[];
  y_list: number[];
  color: string;
  width: number;
}

interface Arrow {
  type: "arrow";
  x: number;
  y: number;
  dx: number;
  dy: number;
  color: string;
  width: number;
}

interface Polygon {
  type: "polygon";
  x_list: number[];
  y_list: number[];
  color: string;
  width: number;
}

interface Rect {
  type: "rect";
  x: number;
  y: number;
  width: number;
  height: number;
  color: string;
}

interface Circle {
  type: "circle";
  x: number;
  y: number;
  radius: number;
  color: string;
}

interface Text {
  type: "text";
  text: string;
  x: number;
  y: number;
  font_size: number;
  color: string;
  modifiers?: string;
  align?: "left" | "middle" | "right";
}

type VisionObject =
  | RobotYel
  | RobotBlu
  | Ball
  | Line
  | Arrow
  | Polygon
  | Rect
  | Circle
  | Text;

interface FeedData {
  [layerName: string]: { data: VisionObject[]; is_visible: boolean };
}

function drawImageSvg(svg: SVGSVGElement, json: FeedData) {
  svg.innerHTML = "";
  const svgNS = "http://www.w3.org/2000/svg";
  const minSpeed = 10;

  for (const layerName of Object.keys(json).reverse()) {
    const layer = json[layerName];
    if (!layer.is_visible) continue;

    layer.data.forEach((element) => {
      switch (element.type) {
        case "ball": {
          if (
            element.vx &&
            element.vy &&
            Math.sqrt(element.vx ** 2 + element.vy ** 2) > minSpeed
          ) {
            const color = "#ffb325";
            const markerId = `arrow-${color.replace("#", "")}`;
            createArrowMarker(svg, color, markerId);

            const arrow = document.createElementNS(svgNS, "line");
            arrow.setAttribute("x1", element.x.toString());
            arrow.setAttribute("y1", (-element.y).toString());
            arrow.setAttribute("x2", (element.x + element.vx).toString());
            arrow.setAttribute("y2", (-element.y - element.vy).toString());
            arrow.setAttribute("stroke-width", "20");
            arrow.setAttribute("stroke", color);
            arrow.setAttribute("marker-end", `url(#${markerId})`);
            svg.appendChild(arrow);
          }
          const circle = document.createElementNS(svgNS, "circle");
          circle.setAttribute("cx", element.x.toString());
          circle.setAttribute("cy", (-element.y).toString());
          circle.setAttribute("r", "25");
          circle.setAttribute("fill", "#FF7000");
          svg.appendChild(circle);
          break;
        }
        case "robot_blu": {
          if (
            element.vx &&
            element.vy &&
            Math.sqrt(element.vx ** 2 + element.vy ** 2) > minSpeed
          ) {
            const color = "#ffb325";
            const markerId = `arrow-${color.replace("#", "")}`;
            createArrowMarker(svg, color, markerId);

            const arrow = document.createElementNS(svgNS, "line");
            arrow.setAttribute("x1", element.x.toString());
            arrow.setAttribute("y1", (-element.y).toString());
            arrow.setAttribute("x2", (element.x + element.vx).toString());
            arrow.setAttribute("y2", (-element.y - element.vy).toString());
            arrow.setAttribute("stroke-width", "20");
            arrow.setAttribute("stroke", color);
            arrow.setAttribute("marker-end", `url(#${markerId})`);
            svg.appendChild(arrow);
          }
          const robot = document.createElementNS(svgNS, "image");

          robot.setAttribute("x", (element.x - 90).toString());
          robot.setAttribute("y", (-element.y - 90).toString());
          robot.setAttribute(
            "transform",
            `rotate(${-((element.rotation || 0) * 180) / Math.PI}, ${
              element.x
            }, ${-element.y})`
          );
          robot.setAttribute("width", "160");
          robot.setAttribute("height", "180");
          robot.setAttribute("href", "../../images/robot_blu.svg");
          svg.appendChild(robot);

          const text = document.createElementNS(svgNS, "text");
          text.setAttribute("x", element.x.toString());
          text.setAttribute("y", (-element.y).toString());
          text.setAttribute("fill", "white");
          text.setAttribute("text-anchor", "middle");
          text.setAttribute("dominant-baseline", "middle");
          text.setAttribute("dy", "0.1em");
          text.setAttribute("font-size", "150");
          text.setAttribute("font-weight", "bold");
          text.textContent = String(element.robot_id);
          svg.appendChild(text);

          break;
        }
        case "robot_yel": {
          if (
            element.vx &&
            element.vy &&
            Math.sqrt(element.vx ** 2 + element.vy ** 2) > minSpeed
          ) {
            const color = "#ffb325";
            const markerId = `arrow-${color.replace("#", "")}`;
            createArrowMarker(svg, color, markerId);

            const arrow = document.createElementNS(svgNS, "line");
            arrow.setAttribute("x1", element.x.toString());
            arrow.setAttribute("y1", (-element.y).toString());
            arrow.setAttribute("x2", (element.x + element.vx).toString());
            arrow.setAttribute("y2", (-element.y - element.vy).toString());
            arrow.setAttribute("stroke-width", "20");
            arrow.setAttribute("stroke", color);
            arrow.setAttribute("marker-end", `url(#${markerId})`);
            svg.appendChild(arrow);
          }
          const robot = document.createElementNS(svgNS, "image");

          robot.setAttribute("x", (element.x - 90).toString());
          robot.setAttribute("y", (-element.y - 90).toString());
          robot.setAttribute(
            "transform",
            `rotate(${-((element.rotation || 0) * 180) / Math.PI}, ${
              element.x
            }, ${-element.y})`
          );
          robot.setAttribute("width", "160");
          robot.setAttribute("height", "180");
          robot.setAttribute("href", "../../images/robot_yel.svg");
          svg.appendChild(robot);

          const text = document.createElementNS(svgNS, "text");
          text.setAttribute("x", element.x.toString());
          text.setAttribute("y", (-element.y).toString());
          text.setAttribute("fill", "black");
          text.setAttribute("text-anchor", "middle");
          text.setAttribute("dominant-baseline", "middle");
          text.setAttribute("dy", "0.1em");
          text.setAttribute("font-size", "150");
          text.setAttribute("font-weight", "bold");
          text.textContent = String(element.robot_id);
          svg.appendChild(text);

          break;
        }
        case "line": {
          const points: string[] = [];
          for (let i = 0; i < element.x_list.length; i++) {
            points.push(`${element.x_list[i]},${-element.y_list[i]}`);
          }
          const polyline = document.createElementNS(svgNS, "polyline");
          polyline.setAttribute("points", points.join(" "));
          polyline.setAttribute("fill", "none");
          polyline.setAttribute("stroke", element.color || "white");
          polyline.setAttribute("stroke-width", String(element.width || 2));
          svg.appendChild(polyline);
          break;
        }
        case "arrow": {
          const color = element.color;
          const markerId = `arrow-${color.replace("#", "")}`;
          createArrowMarker(svg, color, markerId);

          const line = document.createElementNS(svgNS, "line");
          line.setAttribute("x1", element.x.toString());
          line.setAttribute("y1", (-element.y).toString());
          line.setAttribute("x2", (element.x + element.dx).toString());
          line.setAttribute("y2", (-(element.y + element.dy)).toString());
          line.setAttribute("stroke", color);
          line.setAttribute("stroke-width", String(element.width || 2));
          line.setAttribute("marker-end", `url(#${markerId})`);
          svg.appendChild(line);
          break;
        }
        case "polygon": {
          const points: string[] = [];
          for (let i = 0; i < element.x_list.length; i++) {
            points.push(`${element.x_list[i]},${-element.y_list[i]}`);
          }
          const polygon = document.createElementNS(svgNS, "polygon");
          polygon.setAttribute("points", points.join(" "));
          polygon.setAttribute("fill", element.color);
          polygon.setAttribute("stroke", element.color || "white");
          polygon.setAttribute("stroke-width", String(element.width));
          svg.appendChild(polygon);
          break;
        }
        case "rect": {
          const rect = document.createElementNS(svgNS, "rect");
          rect.setAttribute("x", element.x.toString());
          rect.setAttribute("y", (-element.y - element.height).toString());
          rect.setAttribute("width", String(element.width));
          rect.setAttribute("height", String(element.height));
          rect.setAttribute("fill", element.color);
          svg.appendChild(rect);
          break;
        }
        case "circle": {
          const circle = document.createElementNS(svgNS, "circle");
          circle.setAttribute("cx", element.x.toString());
          circle.setAttribute("cy", (-element.y).toString());
          circle.setAttribute("r", String(element.radius));
          circle.setAttribute("fill", element.color);
          svg.appendChild(circle);
          break;
        }
        case "text": {
          const text = document.createElementNS(svgNS, "text");
          text.textContent = element.text;
          text.setAttribute("x", element.x.toString());
          text.setAttribute("y", (-element.y).toString());
          text.setAttribute("fill", element.color || "white");
          text.setAttribute("font-size", String(element.font_size));
          text.setAttribute("text-anchor", element.align || "middle");
          if (element.modifiers) text.setAttribute("style", element.modifiers);
          svg.appendChild(text);
          break;
        }
        default:
          // @ts-ignore
          console.warn("Unknown element type:", element.type);
      }
    });
  }
}

function createArrowMarker(svg: SVGSVGElement, color: string, id: string) {
  const existing = svg.querySelector(`#${id}`);
  if (existing) return;

  const svgNS = "http://www.w3.org/2000/svg";
  const defs =
    svg.querySelector("defs") ||
    (() => {
      const d = document.createElementNS(svgNS, "defs");
      svg.appendChild(d);
      return d;
    })();
  const marker = document.createElementNS(svgNS, "marker");
  marker.setAttribute("id", id);
  marker.setAttribute("markerWidth", "4");
  marker.setAttribute("markerHeight", "3");
  marker.setAttribute("refX", "0");
  marker.setAttribute("refY", "1.5");
  marker.setAttribute("orient", "auto");

  const polygon = document.createElementNS(svgNS, "polygon");
  polygon.setAttribute("points", "0 0, 4 1.5, 0 3");
  polygon.setAttribute("fill", color);

  marker.appendChild(polygon);
  defs.appendChild(marker);
}
