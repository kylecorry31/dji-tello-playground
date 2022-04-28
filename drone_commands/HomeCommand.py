import math

from commands import Command, CommandRunner
from drone.tello import Tello
from drone_commands import RotateCommand


class HomeCommand(Command):
    def __init__(self, drone: Tello):
        super().__init__(drone)
        self.drone = drone

    def initialize(self):
        position = self.drone.position.read()
        angle = math.atan2(position[1], position[0])
        rotation = math.degrees(angle)
        print(rotation)
        CommandRunner.get_instance().schedule(RotateCommand(self.drone, rotation, relative=False))

    def is_finished(self):
        return True
