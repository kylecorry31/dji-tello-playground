from commands import Command
from drone.drone import Drone


class EmergencyCommand(Command):
    def __init__(self, drone: Drone):
        super().__init__(drone)
        self.drone = drone

    def initialize(self):
        self.drone.emergency_stop()

    def is_finished(self):
        return False