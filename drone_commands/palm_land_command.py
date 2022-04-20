from commands.command import Command
from drone.drone import Drone


class PalmLandCommand(Command):

    def __init__(self, drone: Drone):
        super().__init__(drone)
        self.drone = drone

    def initialize(self):
        self.drone.land(True)

    def is_finished(self):
        return not self.drone.is_flying()

    def end(self, interrupted):
        self.drone.stop()
