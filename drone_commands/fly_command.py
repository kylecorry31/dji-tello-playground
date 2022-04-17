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

    def execute(self):
        z = (self.controller.get_trigger(RT) - self.controller.get_trigger(LT)) * self.z_speed
        x = self.controller.get_x(RIGHT_STICK) * self.x_speed
        y = self.controller.get_y(RIGHT_STICK) * self.y_speed
        yaw = self.controller.get_x(LEFT_STICK) * self.yaw_speed

        self.drone.fly(x, y, z, yaw)

    def is_finished(self):
        return False

    def end(self, interrupted):
        self.drone.stop()
