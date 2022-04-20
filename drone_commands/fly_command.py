from controller.xbox_controller import *
from drone.drone import Drone


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
        self.last_d_up = False

    def execute(self):
        d_up = self.controller.get_button(LEFT_THUMB)
        if d_up != self.last_d_up and d_up:
            self.is_field_oriented = not self.is_field_oriented
            print("Field oriented?:", self.is_field_oriented)
        z = (self.controller.get_trigger(RT) - self.controller.get_trigger(LT)) * self.z_speed
        x = self.controller.get_x(RIGHT_STICK) * self.x_speed
        y = self.controller.get_y(RIGHT_STICK) * self.y_speed
        yaw = self.controller.get_x(LEFT_STICK) * self.yaw_speed
        fast_mode = self.controller.get_button(RIGHT_THUMB)
        self.last_d_up = d_up
        self.drone.fly(x, y, z, yaw, self.is_field_oriented, fast_mode)

    def is_finished(self):
        return False

    def end(self, interrupted):
        self.drone.stop()
