export function getRobotControlDataControlDecoder(
    robotControlTeam,
    robotControlId,
    speed_x,
    speed_y,
    speed_r
) {
    let data = {
        control: "actuate_robot",
        data: {
            isteamyellow: robotControlTeam === "yellow",
            robot_commands: [
                {
                    robot_id: robotControlId,
                    forward_vel: speed_x,
                    left_vel: -speed_y,
                    angular: speed_r,
                    angle: 0,
                    kick_up: 0,
                    kick_forward: 0,
                    auto_kick_up: 0,
                    auto_kick_forward: 0,
                    kicker_setting: 0,
                    dribbler_setting: 0,
                },
            ],
        },
    };

    return data;
}

export function getRobotControlDataTransnet(
    robotControlTeam,
    robotControlId,
    speed_x,
    speed_y,
    speed_r
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