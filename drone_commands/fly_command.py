from controller.xbox_controller import *
from drone.drone import Drone
from drone.modules.altitude_hold_module import AltitudeHoldModule
from drone.modules.headless_module import HeadlessModule
from drone.modules.speed_limit_module import SpeedLimitModule
from filter.pid import PID


class FlyCommand(Command):

    def __init__(self, drone: Drone, controller: XboxController):
        super().__init__(drone)
        self.drone = drone
        self.controller = controller
        self.last_thumb = False
        self.headless_module = HeadlessModule(self.drone.compass)
        self.headless_module.is_enabled = False
        self.altitude_hold_module = AltitudeHoldModule(self.drone.altimeter)
        self.speed_limit_module = SpeedLimitModule(1.0, True)

    def initialize(self):
        self.headless_module.reset()
        self.altitude_hold_module.reset()
        self.speed_limit_module.reset()

    def execute(self):
        self.__update_headless()
        z = self.controller.get_trigger(RT) - self.controller.get_trigger(LT)
        x = self.controller.get_x(RIGHT_STICK)
        y = self.controller.get_y(RIGHT_STICK)
        yaw = self.controller.get_x(LEFT_STICK)
        fast_mode = self.controller.get_button(RIGHT_THUMB)
        self.drone.fly(x, y, z, yaw, fast_mode)

    def __fly(self, x: float, y: float, z: float, yaw: float, fast_mode: bool):
        modules = [self.headless_module, self.altitude_hold_module, self.speed_limit_module]
        for module in modules:
            if module.is_enabled:
                (x, y, z, yaw, fast_mode) = module.run(x, y, z, yaw, fast_mode)
        self.drone.fly(x, y, z, yaw, fast_mode)

    def __update_headless(self):
        thumb = self.controller.get_button(LEFT_THUMB)
        if thumb != self.last_thumb and thumb:
            was_enabled = self.headless_module.is_enabled
            self.headless_module.is_enabled = not was_enabled
            if not was_enabled:
                self.headless_module.reset()
            print("Headless?:", self.headless_module.is_enabled)
        self.last_thumb = thumb

    def is_finished(self):
        return False

    def end(self, interrupted):
        self.drone.stop()
