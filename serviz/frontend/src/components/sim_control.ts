import Component from "../loadComponents";
import { sendMessage } from "../socketManager";
import { CustomDropdown, NumberInput } from "../customButtons";

const SimControl: Component = {
  name: "SimControl",
  factory: (container) => {
    container.element.style.position = "relative";
    container.element.style.overflowY = "auto";

    const upHeader = document.createElement("h3");
    upHeader.textContent = "Formations for simulator";
    upHeader.style.padding = "5px 10px";
    upHeader.style.background = "#1a1a1a";
    upHeader.style.display = "flex";
    upHeader.style.flexDirection = "row";
    upHeader.style.height = "auto";
    upHeader.style.width = "auto";
    upHeader.style.userSelect = "none";
    container.element.append(upHeader);

    const firstRow = document.createElement("div");
    firstRow.style.display = "flex";
    firstRow.style.justifyContent = "space-between";
    firstRow.style.width = "90%";
    firstRow.style.margin = "5px 0 0 5%";
    container.element.append(firstRow);

    const btn0 = document.createElement("button");
    btn0.textContent = "0";
    btn0.style.margin = "0";
    btn0.style.width = "40px";
    btn0.style.height = "40px";
    btn0.style.font = "20px Arial, sans-serif";
    firstRow.appendChild(btn0);
    btn0.addEventListener("click", () => {
      sendMessage("send_signal", formations[0]);
    });

    const btn1 = document.createElement("button");
    btn1.textContent = "1";
    btn1.style.cssText = btn0.style.cssText;
    firstRow.appendChild(btn1);
    btn1.addEventListener("click", () => {
      sendMessage("send_signal", formations[1]);
    });

    const btn2 = document.createElement("button");
    btn2.textContent = "2";
    btn2.style.cssText = btn0.style.cssText;
    firstRow.appendChild(btn2);
    btn2.addEventListener("click", () => {
      sendMessage("send_signal", formations[2]);
    });

    const secondRow = document.createElement("div");
    secondRow.style.display = "flex";
    secondRow.style.justifyContent = "center";
    secondRow.style.width = "100%";
    container.element.appendChild(secondRow);

    const randomBtn = document.createElement("button");
    randomBtn.textContent = "Random";
    randomBtn.style.width = "120px";
    randomBtn.style.height = "40px";
    randomBtn.style.font = "20px Arial, sans-serif";
    secondRow.appendChild(randomBtn);
    randomBtn.addEventListener("click", () => {
      sendMessage("send_signal", generateRandomFormation());
    });

    const downHeader = document.createElement("div");
    downHeader.style.display = "flex";
    downHeader.style.alignItems = "center";
    downHeader.style.justifyContent = "space-between";
    downHeader.style.background = "#1a1a1a";
    downHeader.style.padding = "5px 10px";
    downHeader.style.marginTop = "10px";
    downHeader.style.userSelect = "none";

    const title = document.createElement("h3");
    title.textContent = "Robot control";
    title.style.background = "none";
    title.style.margin = "0";
    title.style.padding = "0";
    title.style.color = "#b0b0b0";
    downHeader.appendChild(title);

    const controlCheckbox = document.createElement("input");
    controlCheckbox.type = "checkbox";
    downHeader.appendChild(controlCheckbox);

    container.element.appendChild(downHeader);

    const containerWrapper = document.createElement("div");
    containerWrapper.style.opacity = "0.5";
    containerWrapper.style.pointerEvents = "none";

    controlCheckbox.addEventListener("change", () => {
      if (controlCheckbox.checked) {
        containerWrapper.style.opacity = "1";
        containerWrapper.style.pointerEvents = "auto";
      } else {
        containerWrapper.style.opacity = "0.5";
        containerWrapper.style.pointerEvents = "none";
      }
    });

    const wrapper = document.createElement("div");
    wrapper.style.display = "flex";
    wrapper.style.alignItems = "center";
    wrapper.style.padding = "5px";

    const selectDropdown = new CustomDropdown({
      options: [{ value: "BLUE" }, { value: "YELLOW" }],
      onChange: (value) => {},
    });
    selectDropdown.element.style.width = "50%";
    wrapper.appendChild(selectDropdown.element);

    const selectNumber = new NumberInput();
    selectNumber.element.style.width = "50%";
    wrapper.appendChild(selectNumber.element);
    containerWrapper.appendChild(wrapper);

    const speedLabel = document.createElement("div");
    speedLabel.style.color = "#b0b0b0";
    speedLabel.style.margin = "10px";
    speedLabel.textContent = `Linear speed 1.0 m/s`;
    speedLabel.style.font = "15px Arial, sans-serif";
    containerWrapper.appendChild(speedLabel);

    const speedSlider = document.createElement("input");
    speedSlider.type = "range";
    speedSlider.style.marginLeft = "10px";
    speedSlider.min = "0";
    speedSlider.max = "2";
    speedSlider.step = "0.1";
    speedSlider.value = "1";
    speedSlider.style.width = "calc(100% - 20px)";

    speedSlider.addEventListener("input", () => {
      const value = parseFloat(speedSlider.value);
      speedLabel.textContent = `Linear speed ${value.toFixed(1)} m/s`;
    });
    containerWrapper.appendChild(speedSlider);

    const wSpeedLabel = document.createElement("div");
    wSpeedLabel.style.color = "#b0b0b0";
    wSpeedLabel.style.margin = "10px";
    wSpeedLabel.textContent = `Angular speed 1.5 rad/s`;
    wSpeedLabel.style.font = "15px Arial, sans-serif";
    containerWrapper.appendChild(wSpeedLabel);

    const wSpeedSlider = document.createElement("input");
    wSpeedSlider.type = "range";
    wSpeedSlider.style.marginLeft = "10px";
    wSpeedSlider.min = "0";
    wSpeedSlider.max = "3";
    wSpeedSlider.step = "0.1";
    wSpeedSlider.value = "1.5";
    wSpeedSlider.style.width = "calc(100% - 20px)";

    wSpeedSlider.addEventListener("input", () => {
      const value = parseFloat(wSpeedSlider.value);
      wSpeedLabel.textContent = `Angular speed ${value.toFixed(1)} rad/s`;
    });
    containerWrapper.appendChild(wSpeedSlider);

    container.element.appendChild(containerWrapper);

    const stopRow = document.createElement("div");
    stopRow.style.display = "flex";
    stopRow.style.justifyContent = "center";
    stopRow.style.width = "100%";
    stopRow.style.marginTop = "10px";
    container.element.appendChild(stopRow);

    const stopBtm = document.createElement("button");
    stopBtm.textContent = "Stop robots";
    stopBtm.style.width = "150px";
    stopBtm.style.height = "50px";
    stopBtm.style.font = "24px Arial, sans-serif";
    stopRow.appendChild(stopBtm);
    stopBtm.addEventListener("click", () => {
      let count = 0;
      const intervalId = setInterval(() => {
        count++;
        for (const color of ["blue", "yellow"]) {
          for (let number = 0; number < 16; number++) {
            sendMessage(
              "send_signal",
              getRobotControlDataTransnet(color, number, 0, 0, 0)
            );
          }
        }
        if (count >= 20) {
          clearInterval(intervalId);
        }
      }, 50);
    });

    const pressedKeys: Set<string> = new Set();
    window.addEventListener("keydown", (e: KeyboardEvent) => {
      pressedKeys.add(e.code);
    });
    window.addEventListener("keyup", (e: KeyboardEvent) => {
      pressedKeys.delete(e.code);
    });

    function controlRobot(): void {
      let speed_x: number = 0;
      let speed_y: number = 0;
      let speed_r: number = 0;

      const chosen_vel_xy: number = parseFloat(speedSlider.value);
      const chosen_vel_r: number = parseFloat(wSpeedSlider.value);

      const dirs: {
        key: string;
        speed_x: number;
        speed_y: number;
        speed_r: number;
      }[] = [
        { key: "KeyW", speed_x: chosen_vel_xy, speed_y: 0, speed_r: 0 },
        { key: "KeyA", speed_x: 0, speed_y: -chosen_vel_xy, speed_r: 0 },
        { key: "KeyS", speed_x: -chosen_vel_xy, speed_y: 0, speed_r: 0 },
        { key: "KeyD", speed_x: 0, speed_y: chosen_vel_xy, speed_r: 0 },
        { key: "KeyQ", speed_x: 0, speed_y: 0, speed_r: chosen_vel_r },
        { key: "KeyE", speed_x: 0, speed_y: 0, speed_r: -chosen_vel_r },
      ];

      for (const dir of dirs) {
        if (pressedKeys.has(dir.key)) {
          speed_x += dir.speed_x;
          speed_y += dir.speed_y;
          speed_r += dir.speed_r;
        }
      }

      const chosen_color: string = selectDropdown.getValue().toLowerCase();
      const chosen_number: number = parseFloat(selectNumber.getValue());

      const data = getRobotControlDataTransnet(
        chosen_color,
        chosen_number,
        speed_x,
        speed_y,
        speed_r
      );
      sendMessage("send_signal", data);
    }
    setInterval(() => {
      if (controlCheckbox.checked) {
        controlRobot();
      }
    }, 50);
  },
};

export default SimControl;

function getRobotControlDataTransnet(
  robotControlTeam: string,
  robotControlId: number,
  speed_x: number,
  speed_y: number,
  speed_r: number
) {
  let data = {
    transnet: "actuate_robot",
    data: {
      isteamyellow: robotControlTeam === "yellow",
      robot_commands: [
        {
          id: robotControlId,
          move_command: {
            local_velocity: {
              forward: speed_x,
              left: -speed_y,
              angular: speed_r,
            },
          },
          kick_speed: 0,
          kick_angle: 0,
          dribbler_speed: 0,
        },
      ],
    },
  };
  return data;
}

let formations = [
  {
    // default
    transnet: "set_formation",
    data: {
      BLUE: [
        { robot_id: 0, x: -1500, y: 1120, rotation: 0 },
        { robot_id: 1, x: -1500, y: 0, rotation: 0 },
        { robot_id: 2, x: -1500, y: -1120, rotation: 0 },
        { robot_id: 3, x: -550, y: 0, rotation: 0 },
        { robot_id: 4, x: -2500, y: 0, rotation: 0 },
        { robot_id: 5, x: -3600, y: 0, rotation: 0 },
      ],
      YELLOW: [
        { robot_id: 0, x: 1500, y: 1120, rotation: 180 },
        { robot_id: 1, x: 1500, y: 0, rotation: 180 },
        { robot_id: 2, x: 1500, y: -1120, rotation: 180 },
        { robot_id: 3, x: 550, y: 0, rotation: 180 },
        { robot_id: 4, x: 2500, y: 0, rotation: 180 },
        { robot_id: 5, x: 3600, y: 0, rotation: 180 },
      ],
      BALL: { x: 0, y: 0, vx: 0, vy: 0 },
      enable_graveyard: true,
    },
  },
  {
    // line
    transnet: "set_formation",
    data: {
      BLUE: [
        { robot_id: 0, x: -2000, y: 1000, rotation: 0 },
        { robot_id: 1, x: -2000, y: 600, rotation: 0 },
        { robot_id: 2, x: -2000, y: 200, rotation: 0 },
        { robot_id: 3, x: -2000, y: -200, rotation: 0 },
        { robot_id: 4, x: -2000, y: -600, rotation: 0 },
        { robot_id: 5, x: -2000, y: -1000, rotation: 0 },
      ],
      YELLOW: [
        { robot_id: 0, x: 2000, y: 1000, rotation: 180 },
        { robot_id: 1, x: 2000, y: 600, rotation: 180 },
        { robot_id: 2, x: 2000, y: 200, rotation: 180 },
        { robot_id: 3, x: 2000, y: -200, rotation: 180 },
        { robot_id: 4, x: 2000, y: -600, rotation: 180 },
        { robot_id: 5, x: 2000, y: -1000, rotation: 180 },
      ],
      BALL: { x: 0, y: 0, vx: 0, vy: 0 },
      enable_graveyard: true,
    },
  },
  {
    // graveyard
    transnet: "set_formation",
    data: {
      enable_graveyard: true,
    },
  },
];

function generateRandomFormation() {
  const randomRobot = (id: number) => ({
    robot_id: id,
    x: Math.random() * 8000 - 4000,
    y: Math.random() * 6000 - 3000,
    rotation: Math.random() * 360,
  });

  return {
    transnet: "set_formation",
    data: {
      BLUE: Array.from({ length: 6 }, (_, i) => randomRobot(i)),
      YELLOW: Array.from({ length: 6 }, (_, i) => randomRobot(i)),
      BALL: { x: 0, y: 0, vx: 0, vy: 0 },
      enable_graveyard: false,
    },
  };
}
