from commands.command import Command
from drone.drone import Drone
import time


class FlipBackwardCommand(Command):

    def __init__(self, drone: Drone):
        super().__init__(drone)
        self.drone = drone
        self.start_time = None

    def initialize(self):
        self.drone.flip_back()
        self.start_time = time.time()

    def is_finished(self):
        return time.time() - self.start_time > 0.5

    def end(self, interrupted):
        self.drone.stop()
