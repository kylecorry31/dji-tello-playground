from commands.command import Command
from drone.drone import Drone
from utils import clamp, delta_angle
import time


class RotateCommand(Command):

    def __init__(self, drone: Drone, yaw: float, relative=True):
        super().__init__(drone)
        self.drone = drone
        self.start_time = None
        self.yaw = yaw
        self.start_yaw = None
        self.relative = relative
        self.estimated_time = None

    def initialize(self):
        self.start_yaw = self.drone.get_yaw()
        self.start_time = time.time()
        self.estimated_time = abs(self.get_error()) / 65

    def execute(self):
        error = self.get_error()
        self.drone.fly(0, 0, 0, clamp(error * 0.05, -1, 1))

    def is_finished(self):
        expired = time.time() - self.start_time >= self.estimated_time
        at_target = abs(self.get_error()) <= 1
        return at_target or expired

    def end(self, interrupted):
        self.drone.stop()

    def get_error(self):
        if self.relative:
            return self.yaw - self.get_yaw()
        return delta_angle(self.drone.get_yaw(), self.yaw)

    def get_yaw(self):
        return self.drone.get_yaw() - self.start_yaw
