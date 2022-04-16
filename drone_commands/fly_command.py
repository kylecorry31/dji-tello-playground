from controller.xbox_controller import *
from drone.drone import Drone


class FlyCommand(Command):

    def __init__(self, drone: Drone, controller: XboxController):
        super().__init__(drone)
        self.drone = drone
        self.controller = controller
        self.x_speed = 100
        self.y_speed = 100
        self.z_speed = 100
        self.yaw_speed = 100

    def execute(self):
        self.drone.z_velocity = (self.controller.get_trigger(RT) - self.controller.get_trigger(LT)) * self.z_speed
        self.drone.x_velocity = self.controller.get_x(RIGHT_STICK) * self.x_speed
        self.drone.y_velocity = self.controller.get_y(RIGHT_STICK) * self.y_speed
        self.drone.yaw_velocity = self.controller.get_x(LEFT_STICK) * self.yaw_speed

        self.drone.fly()

    def is_finished(self):
        return False

    def end(self, interrupted):
        self.drone.stop()
