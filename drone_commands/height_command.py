from commands.command import Command
from drone.drone import Drone
from utils import clamp
import time


class HeightCommand(Command):

    def __init__(self, drone: Drone, height: float, relative=True):
        super().__init__(drone)
        self.drone = drone
        self.start_time = None
        self.height = height
        self.start_height = None
        self.relative = relative
        self.estimated_time = None

    def initialize(self):
        self.start_height = self.drone.get_height()
        self.start_time = time.time()
        self.estimated_time = abs(self.get_error()) / 65

    def execute(self):
        error = self.get_error()
        self.drone.fly(0, 0, clamp(error * 0.05, -1, 1), 0)

    def is_finished(self):
        expired = time.time() - self.start_time >= self.estimated_time
        at_target = abs(self.get_error()) <= 2
        return at_target or expired

    def end(self, interrupted):
        self.drone.stop()

    def get_error(self):
        if self.relative:
            return self.height - self.get_height()
        return self.height - self.drone.get_tof()

    def get_height(self):
        return self.drone.get_height() - self.start_height
