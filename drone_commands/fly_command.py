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
        self.handle_field_orientation()
        z_adjust = self.handle_altitude_maintain()
        z = (self.controller.get_trigger(RT) - self.controller.get_trigger(LT)) * self.z_speed
        if abs(z) < 0.1:
            z = z_adjust
        else:
            self.maintain_height = None
        x = self.controller.get_x(RIGHT_STICK) * self.x_speed
        y = self.controller.get_y(RIGHT_STICK) * self.y_speed
        yaw = self.controller.get_x(LEFT_STICK) * self.yaw_speed
        fast_mode = self.controller.get_button(RIGHT_THUMB)
        self.last_time = time.time()
        self.drone.fly(x, y, z, yaw, self.is_field_oriented, fast_mode)

    def handle_altitude_maintain(self):
        dt = time.time() - self.last_time
        if self.controller.get_button(X):
            self.maintain_height = self.drone.altimeter.read()
            print("Maintain height:", self.maintain_height)

        if self.maintain_height is None:
            return 0

        return self.maintain_pid.calculate(self.drone.altimeter.read(), self.maintain_height, dt)

    def handle_field_orientation(self):
        thumb = self.controller.get_button(LEFT_THUMB)
        if thumb != self.last_thumb and thumb:
            self.is_field_oriented = not self.is_field_oriented
            print("Field oriented?:", self.is_field_oriented)
        self.last_thumb = thumb

    def is_finished(self):
        return False

    def end(self, interrupted):
        self.drone.stop()
