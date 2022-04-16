from controller.xbox_controller import *
from drone.drone import Drone


class FlyCommand(Command):

    def __init__(self, drone: Drone, controller: XboxController):
        super().__init__(drone)
        self.drone = drone
        self.controller = controller
        self.x_speed = 50
        self.y_speed = 50
        self.z_speed = 50
        self.yaw_speed = 50

    def execute(self):
        if self.controller.get_button(LB):
            self.drone.z_velocity = -self.z_speed
        elif self.controller.get_button(RB):
            self.drone.z_velocity = self.z_speed
        else:
            self.drone.z_velocity = 0

        self.drone.x_velocity = self.controller.get_x(RIGHT_STICK) * self.x_speed
        self.drone.y_velocity = self.controller.get_y(RIGHT_STICK) * self.y_speed
        self.drone.yaw_velocity = self.controller.get_x(LEFT_STICK) * self.yaw_speed

        self.drone.fly()

    def is_finished(self):
        return False

    def end(self, interrupted):
        self.drone.stop()
