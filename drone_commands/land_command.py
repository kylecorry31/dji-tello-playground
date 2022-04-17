from commands.command import Command
from drone.drone import Drone


class LandCommand(Command):

    def __init__(self, drone: Drone):
        super().__init__(drone)
        self.drone = drone

    def initialize(self):
        if self.is_finished():
            return
        self.drone.land()

    def is_finished(self):
        return not self.drone.is_flying()

    def end(self, interrupted):
        if interrupted:
            self.drone.stop()
