from commands import Command
from drone.drone import Drone


class SensorUpdateCommand(Command):
    def __init__(self, drone: Drone):
        super().__init__(None)
        self.drone = drone

    def initialize(self):
        self.drone.reset_sensors()

    def execute(self):
        self.drone.update_sensors()

    def is_finished(self):
        return False
