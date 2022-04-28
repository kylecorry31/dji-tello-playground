from commands import Command
from drone.drone import Drone


class ToggleAltitudeHoldCommand(Command):
    def __init__(self, drone: Drone):
        super().__init__(None)
        self.drone = drone

    def initialize(self):
        self.drone.hold_altitude(not self.drone.is_holding_altitude())

    def is_finished(self):
        return True
