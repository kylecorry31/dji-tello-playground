from commands import Command
from drone.drone import Drone


class ToggleHeadlessCommand(Command):
    def __init__(self, drone: Drone):
        super().__init__(None)
        self.drone = drone

    def initialize(self):
        self.drone.set_headless(not self.drone.is_headless())

    def is_finished(self):
        return True
