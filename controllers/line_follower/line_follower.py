from controller import Robot

class LineFollower(Robot):
    def __init__(self):
        super().__init__()

        self.timestep = int(self.getBasicTimeStep())

        self.left_motor = self.getDevice("left wheel motor")
        self.right_motor = self.getDevice("right wheel motor")

        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))

        # Sensors
        self.ds_left = self.getDevice("DS_Left")
        self.ds_right = self.getDevice("DS_Right")

        self.ds_left.enable(self.timestep)
        self.ds_right.enable(self.timestep)

    def move_forward(self, speed=4.0):
        self.left_motor.setVelocity(speed)
        self.right_motor.setVelocity(speed)

    def turn_left(self, speed=4.0):
        self.left_motor.setVelocity(speed)
        self.right_motor.setVelocity(-speed)

    def turn_right(self, speed=4.0):
        self.left_motor.setVelocity(-speed)
        self.right_motor.setVelocity(speed)

    def stop(self):
        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)


if __name__ == "__main__":
    robot = LineFollower()
    black_color = 999 # less than
    while robot.step(robot.timestep) != -1:

        # Print sensor values
        left_sensor_value = robot.ds_left.getValue()
        right_sensor_value = robot.ds_right.getValue()
        print(
            "Left:", left_sensor_value,
            " Right:", right_sensor_value
        )


        if left_sensor_value >= black_color and right_sensor_value >= black_color:
            robot.move_forward()
        elif left_sensor_value >= black_color:
            robot.turn_left()
        elif right_sensor_value >= black_color:
            robot.turn_right()
        else:
            robot.stop()