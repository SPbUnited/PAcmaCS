#! /bin/env python3

robot_template = \
"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg version = "1.1"
     baseProfile="full"
     xmlns = "http://www.w3.org/2000/svg"
     xmlns:xlink = "http://www.w3.org/1999/xlink"
     xmlns:ev = "http://www.w3.org/2001/xml-events"
     height = "180px"  width = "160px">
     <circle cx="90" cy="90" r="90" fill="ROBOT_COLOR" stroke="none" stroke-width="5px"/>
     <circle cx="90" cy="90" r="88.5" fill="black" stroke="none" stroke-width="5px"/>
     <rect x="158.5" y="34" width="5" height="112" fill="ROBOT_COLOR"/>
     <circle cx="90" cy="90" r="25" fill="ROBOT_COLOR" stroke="none" stroke-width="5px"/>

     <!-- <rect x="120" y="80" width="40" height="20" /> -->

     <circle cx="125" cy="35" r="20" fill="ROBOT_ID_0" stroke="none" stroke-width="5px"/>
     <circle cx="125" cy="145" r="20" fill="ROBOT_ID_1" stroke="none" stroke-width="5px"/>
     <circle cx="35" cy="125" r="20" fill="ROBOT_ID_2" stroke="none" stroke-width="5px"/>
     <circle cx="35" cy="55" r="20" fill="ROBOT_ID_3" stroke="none" stroke-width="5px"/>
</svg>
"""

g = "lime"
p = "#ff00ff"

robot_id_map = \
{
    0:  [p,p,p,g],
    1:  [g,p,p,g],
    2:  [g,g,p,g],
    3:  [p,g,p,g],
    4:  [p,p,g,p],
    5:  [g,p,g,p],
    6:  [g,g,g,p],
    7:  [p,g,g,p],
    8:  [g,g,g,g],
    9:  [p,p,p,p],
    10: [p,p,g,g],
    11: [g,g,p,p],
    12: [g,p,g,g],
    13: [g,p,p,p],
    14: [p,g,g,g],
    15: [p,g,p,p],
}

def gen_robot(robot_id, robot_color):
    # Substitute robot_id and robot_color in robot_template
    robot = robot_template

    robot = robot.replace("ROBOT_COLOR", robot_color)

    for i in range(4):
        id_string = "ROBOT_ID_" + str(i)
        robot = robot.replace(id_string, robot_id_map[robot_id][i])
    return robot

def save_svg(svg, filename):
    with open(filename, "w") as f:
        f.write(svg)

if __name__ == "__main__":
    robot_dir = "robots/"

    for robot_id in range(16):
        for robot_color in ["yellow", "blue"]:
            robot_svg = gen_robot(robot_id, robot_color)
            save_svg(robot_svg, robot_dir + robot_color[0] + str(robot_id) + ".svg")
