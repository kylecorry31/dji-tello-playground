from commands.command import Command
from drone.drone import Drone


class ResetHeadingCommand(Command):

    def __init__(self, drone: Drone):
        super().__init__(None)
        self.drone = drone

    def initialize(self):
        self.drone.reset_heading()

    def is_finished(self):
        return True
