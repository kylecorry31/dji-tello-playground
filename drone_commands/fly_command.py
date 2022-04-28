from controller.xbox_controller import *
from drone.tello import Tello


class FlyCommand(Command):

    def __init__(self, drone: Tello, controller: XboxController):
        super().__init__(drone)
        self.drone = drone
        self.controller = controller

    def execute(self):
        z = self.controller.get_trigger(RT) - self.controller.get_trigger(LT)
        x = self.controller.get_x(RIGHT_STICK)
        y = self.controller.get_y(RIGHT_STICK)
        yaw = self.controller.get_x(LEFT_STICK)
        fast_mode = self.controller.get_button(RIGHT_THUMB)
        self.drone.fly(x, y, z, yaw, fast_mode, True)

    def is_finished(self):
        return False

    def end(self, interrupted):
        self.drone.stop()
