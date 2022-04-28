from commands.command import Command
import time

from drone.tello import Tello


class FlipCommand(Command):

    def __init__(self, drone: Tello, direction: int):
        super().__init__(drone)
        self.drone = drone
        self.start_time = None
        self.direction = direction

    def initialize(self):
        self.drone.flip(self.direction)
        self.start_time = time.time()

    def is_finished(self):
        return time.time() - self.start_time > 0.5

    def end(self, interrupted):
        self.drone.stop()
