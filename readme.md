# Line Follower Webots

This project is a Webots simulation of a line-following robot built around the Microbot robot model. I added two infrared distance sensors through the robot extension slot so the controller can detect the line and steer the robot automatically.

## Project Overview

- Robot model: Microbot
- Controller: `controllers/line_follower/line_follower.py`
- World file: `worlds/part1_make_line_follower.wbt`
- Sensors added through the extension slot:
	- `DS_Left`
	- `DS_Right`

The robot follows a dark line on the track by comparing the values returned by the left and right sensors.

## How It Works

The controller reads both infrared sensors on every simulation step and uses a simple decision rule:

- If both sensors see the line, the robot moves forward.
- If only the left sensor sees the line, the robot turns left.
- If only the right sensor sees the line, the robot turns right.
- If neither sensor sees the line, the robot stops.

## Files

- `controllers/line_follower/line_follower.py` - Python controller for the line follower logic.
- `protos/Microbot.proto` - Microbot prototype with extension slot support.
- `worlds/part1_make_line_follower.wbt` - Webots world used for the simulation.

## Sensor Setup

The Microbot robot uses its `extensionSlot` field to attach the two infrared distance sensors:

- `DS_Left` on the left side
- `DS_Right` on the right side

These sensors are configured as `infra-red` distance sensors and are enabled in the controller.

## Running The Simulation

1. Open `worlds/part1_make_line_follower.wbt` in Webots.
2. Run the simulation.
3. Open the controller output to watch the sensor values and robot decisions.

## Notes

- The track is designed for line following in the Webots environment.
- The controller uses a fixed threshold to distinguish the dark line from the background.
