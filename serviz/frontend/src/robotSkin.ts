import { bus } from "./socketManager";

export type RobotSkinMode = "default" | "id_pattern";

const ROBOT_SKIN_MODE_KEY = "robotSkinMode";

export function getRobotSkinMode(): RobotSkinMode {
  try {
    const mode = localStorage.getItem(ROBOT_SKIN_MODE_KEY);
    return mode === "id_pattern" || mode === "default" ? mode : "default";
  } catch {
    return "default";
  }
}

export function setRobotSkinMode(mode: RobotSkinMode): void {
  localStorage.setItem(ROBOT_SKIN_MODE_KEY, mode);
  bus.emit("robot_skin_mode_changed", mode);
}

export function getRobotImageHref(
  color: "blue" | "yellow",
  robotId: number,
): string {
  const defaultHref =
    color === "blue"
      ? "../../images/robot_blu.svg"
      : "../../images/robot_yel.svg";

  if (
    getRobotSkinMode() === "default" ||
    !Number.isInteger(robotId) ||
    robotId < 0 ||
    robotId > 15
  ) {
    return defaultHref;
  }

  const prefix = color === "blue" ? "b" : "y";
  return `../../images/robots/${prefix}${robotId}.svg`;
}
