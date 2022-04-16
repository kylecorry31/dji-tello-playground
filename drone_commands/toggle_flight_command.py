from commands.command import Command
from drone.drone import Drone
import time


class ToggleFlightCommand(Command):

    def __init__(self, drone: Drone):
        super().__init__(drone)
        self.drone = drone
        self.start_time = None
        self.is_taking_off = False

    def initialize(self):
        self.is_taking_off = not self.drone.is_flying
        if self.is_taking_off:
            self.drone.takeoff()
        else:
            self.drone.land()
        self.start_time = time.time()

    def is_finished(self):
        # TODO: Base this off of height
        return time.time() - self.start_time > 2

    def end(self, interrupted):
        self.drone.stop()
