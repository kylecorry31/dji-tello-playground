from commands import Command
from drone.tello import Tello


class SensorUpdateCommand(Command):
    def __init__(self, drone: Tello):
        super().__init__(None)
        self.drone = drone

    def initialize(self):
        self.drone.reset_sensors()

    def execute(self):
        self.drone.update_sensors()

    def is_finished(self):
        return False
