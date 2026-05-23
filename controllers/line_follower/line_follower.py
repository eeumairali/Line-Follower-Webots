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
        
        # State tracking to recover when lost or stuck
        # "left", "right", or None
        self.last_direction = None 

    def move_forward(self, speed=4.0):
        self.left_motor.setVelocity(speed)
        self.right_motor.setVelocity(speed)

    def turn_left(self, speed=4.0):
        self.left_motor.setVelocity(-speed)  # Swapped for true pivot spin
        self.right_motor.setVelocity(speed)
        self.last_direction = "left"

    def turn_right(self, speed=4.0):
        self.left_motor.setVelocity(speed)
        self.right_motor.setVelocity(-speed) # Swapped for true pivot spin
        self.last_direction = "right"

    def stop(self):
        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)


if __name__ == "__main__":
    robot = LineFollower()
    
    # Adjust this threshold based on your Webots console print logs
    # Values lower than this mean the sensor is over the black line
    black_threshold = 999 

    while robot.step(robot.timestep) != -1:

        left_val = robot.ds_left.getValue()
        right_val = robot.ds_right.getValue()
        
        print(f"Left: {left_val:.1f} | Right: {right_val:.1f} | Last Turn: {robot.last_direction}")

        # 1. BOTH SENSORS SEE WHITE (Normal straight away OR completely lost)
        if left_val >= black_threshold and right_val >= black_threshold:
            if robot.last_direction == "left":
                # It was turning left, overshot, so spin RIGHT to find the line again
                robot.turn_right()
            elif robot.last_direction == "right":
                # It was turning right, overshot, so spin LEFT to find the line again
                robot.turn_left()
            else:
                # Starting condition: clean floor, just push forward to find a line
                robot.move_forward()

        # 2. LEFT SENSOR HITS BLACK (Robot drifted right)
        elif left_val < black_threshold and right_val >= black_threshold:
            robot.turn_left()

        # 3. RIGHT SENSOR HITS BLACK (Robot drifted left)
        elif right_val < black_threshold and left_val >= black_threshold:
            robot.turn_right()

        # 4. BOTH SENSORS HIT BLACK (Intersection / Loop Continuation)
        else:
            # Instead of stopping, we force it forward so it pushes through 
            # intersections and completes endless loops
            robot.move_forward()