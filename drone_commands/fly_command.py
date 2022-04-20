from controller.xbox_controller import *
from drone.drone import Drone
from filter.pid import PID


class FlyCommand(Command):

    def __init__(self, drone: Drone, controller: XboxController):
        super().__init__(drone)
        self.drone = drone
        self.controller = controller
        self.x_speed = 1.0
        self.y_speed = 1.0
        self.z_speed = 1.0
        self.yaw_speed = 1.0
        self.is_field_oriented = False
        self.last_thumb = False
        self.maintain_height = None
        self.maintain_pid = PID(0.03, 0.0, 0.05)
        self.last_time = None

    def initialize(self):
        self.maintain_pid.reset()
        self.maintain_height = None
        self.last_time = time.time()

    def execute(self):
        self.update_field_orientation()
        z = self.get_z()
        x = self.controller.get_x(RIGHT_STICK) * self.x_speed
        y = self.controller.get_y(RIGHT_STICK) * self.y_speed
        yaw = self.controller.get_x(LEFT_STICK) * self.yaw_speed
        fast_mode = self.controller.get_button(RIGHT_THUMB)
        self.last_time = time.time()
        self.drone.fly(x, y, z, yaw, self.is_field_oriented, fast_mode)

    def get_z(self):
        dt = time.time() - self.last_time
        user = (self.controller.get_trigger(RT) - self.controller.get_trigger(LT)) * self.z_speed

        # If the user is not moving, maintain the height
        if abs(user) < 0.1 and self.maintain_height is not None:
            return self.maintain_pid.calculate(self.drone.altimeter.read(), self.maintain_height, dt)

        # If the user is moving up/down, set the new maintain height
        self.maintain_height = self.drone.altimeter.read()

        # Don't maintain height if it is too high or low
        if self.maintain_height <= 10 or self.maintain_height > 1000:
            self.maintain_height = None

        return user

    def update_field_orientation(self):
        thumb = self.controller.get_button(LEFT_THUMB)
        if thumb != self.last_thumb and thumb:
            self.is_field_oriented = not self.is_field_oriented
            print("Field oriented?:", self.is_field_oriented)
        self.last_thumb = thumb

    def is_finished(self):
        return False

    def end(self, interrupted):
        self.drone.stop()
