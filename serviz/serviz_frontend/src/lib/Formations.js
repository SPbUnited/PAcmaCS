let formations = [
    { // default
        "transnet": "set_formation",
        "data": {
            "BLUE": [
                {"robot_id": 0, "x": -1500, "y": 1120, "rotation": 0},
                {"robot_id": 1, "x": -1500, "y": 0, "rotation": 0},
                {"robot_id": 2, "x": -1500, "y": -1120, "rotation": 0},
                {"robot_id": 3, "x": -550, "y": 0, "rotation": 0},
                {"robot_id": 4, "x": -2500, "y": 0, "rotation": 0},
                {"robot_id": 5, "x": -3600, "y": 0, "rotation": 0},
            ],
            "YELLOW": [
                {"robot_id": 0, "x": 1500, "y": 1120, "rotation": 180},
                {"robot_id": 1, "x": 1500, "y": 0, "rotation": 180},
                {"robot_id": 2, "x": 1500, "y": -1120, "rotation": 180},
                {"robot_id": 3, "x": 550, "y": 0, "rotation": 180},
                {"robot_id": 4, "x": 2500, "y": 0, "rotation": 180},
                {"robot_id": 5, "x": 3600, "y": 0, "rotation": 180},
            ],
            "BALL": {"x": 0, "y": 0, "vx": 0, "vy": 0},
            "enable_graveyard": true,
        }
    },
    { // line
        "transnet": "set_formation",
        "data": {
            "BLUE": [
                {"robot_id": 0, "x": -2000, "y": 1000, "rotation": 0},
                {"robot_id": 1, "x": -2000, "y": 600, "rotation": 0},
                {"robot_id": 2, "x": -2000, "y": 200, "rotation": 0},
                {"robot_id": 3, "x": -2000, "y": -200, "rotation": 0},
                {"robot_id": 4, "x": -2000, "y": -600, "rotation": 0},
                {"robot_id": 5, "x": -2000, "y": -1000, "rotation": 0},
            ],
            "YELLOW": [
                {"robot_id": 0, "x": 2000, "y": 1000, "rotation": 180},
                {"robot_id": 1, "x": 2000, "y": 600, "rotation": 180},
                {"robot_id": 2, "x": 2000, "y": 200, "rotation": 180},
                {"robot_id": 3, "x": 2000, "y": -200, "rotation": 180},
                {"robot_id": 4, "x": 2000, "y": -600, "rotation": 180},
                {"robot_id": 5, "x": 2000, "y": -1000, "rotation": 180},
            ],
            "BALL": {"x": 0, "y": 0, "vx": 0, "vy": 0},
            "enable_graveyard": true,
        }
    },
    { // graveyard
        "transnet": "set_formation",
        "data": {
            "enable_graveyard": true,
        }
    }
];

function generateRandomFormation() {
    let formation = {
        "transnet": "set_formation",
        "data": {
            "BLUE": [],
            "YELLOW": [],
            "BALL": {"x": 0, "y": 0, "vx": 0, "vy": 0},
            "enable_graveyard": false,
        }
    };
    for(let i = 0; i < 6; i++) {
        formation.data.BLUE.push({
            "robot_id": i,
            "x": Math.random() * 8000 - 4000,
            "y": Math.random() * 6000 - 3000,
            "rotation": Math.random() * 360,
        });
        formation.data.YELLOW.push({
            "robot_id": i,
            "x": Math.random() * 8000 - 4000,
            "y": Math.random() * 6000 - 3000,
            "rotation": Math.random() * 360,
        });
    }
    return formation;
}

export function getFormationsCount() {
    return formations.length;
}

export function getFormationData(index) {
    if(index < 0 || index >= formations.length) {
        return generateRandomFormation();
    }
    return formations[index];
}


                        //   {'robot_id': 0, 'rotation': 0.0, 'type': 'robot_blu', 'x': -1499.9638671875, 'y': 1120.0},
                        //   {'robot_id': 1, 'rotation': -0.0, 'type': 'robot_blu', 'x': -1499.9638671875, 'y': 5.2350079132734706e-11},
                        //   {'robot_id': 2, 'rotation': 0.0, 'type': 'robot_blu', 'x': -1499.9638671875, 'y': -1120.0},
                        //   {'robot_id': 3, 'rotation': 0.0, 'type': 'robot_blu', 'x': -549.9639282226562, 'y': -1.1300618427134701e-11},
                        //   {'robot_id': 4, 'rotation': -0.0, 'type': 'robot_blu', 'x': -2499.9638671875, 'y': 3.653068299247497e-12},
                        //   {'robot_id': 5, 'rotation': -0.0, 'type': 'robot_blu', 'x': -3599.9638671875, 'y': -1.5925871732491714e-11},
                        //   {'robot_id': 0, 'rotation': -3.1415927410125732, 'type': 'robot_yel', 'x': 1497.5732421875, 'y': 1120.0},
                        //   {'robot_id': 1, 'rotation': -3.1415927410125732, 'type': 'robot_yel', 'x': 1497.5732421875, 'y': 1.359286641577917e-11},
                        //   {'robot_id': 2, 'rotation': -3.1415927410125732, 'type': 'robot_yel', 'x': 1497.5732421875, 'y': -1120.0},
                        //   {'robot_id': 3, 'rotation': 3.1415927410125732, 'type': 'robot_yel', 'x': 547.5733032226562, 'y': -2.1530442359529722e-12},
                        //   {'robot_id': 4, 'rotation': -3.1415927410125732, 'type': 'robot_yel', 'x': 2497.5732421875, 'y': 2.7035446364259696e-12},
                        //   {'robot_id': 5, 'rotation': -3.1415927410125732, 'type': 'robot_yel', 'x': 3597.5732421875, 'y': -9.58294121139458e-12}],