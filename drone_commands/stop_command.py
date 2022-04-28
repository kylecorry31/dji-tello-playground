from commands.command import Command
from drone.tello import Tello


class StopCommand(Command):

    def __init__(self, drone: Tello):
        super().__init__(drone)
        self.drone = drone

    def initialize(self):
        self.drone.stop()

    def is_finished(self):
        return True

    def end(self, interrupted):
        self.drone.stop()
