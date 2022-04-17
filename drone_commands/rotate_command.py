from commands.command import Command
from drone.drone import Drone
from utils import clamp
import time


class RotateCommand(Command):

    def __init__(self, drone: Drone, yaw: float):
        super().__init__(drone)
        self.drone = drone
        self.start_time = None
        self.yaw = yaw
        self.start_yaw = None
        self.estimated_time = abs(yaw) / 65

    def initialize(self):
        self.start_yaw = self.drone.get_yaw()
        self.start_time = time.time()

    def execute(self):
        error = self.yaw - self.get_yaw()
        self.drone.fly(0, 0, 0, clamp(error * 0.05, -1, 1))

    def is_finished(self):
        expired = time.time() - self.start_time >= self.estimated_time
        at_target = abs(self.yaw - self.get_yaw()) <= 1
        return at_target or expired

    def end(self, interrupted):
        self.drone.stop()

    def get_yaw(self):
        return self.drone.get_yaw() - self.start_yaw
