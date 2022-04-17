from commands import SequentialCommand
from drone.drone import Drone
from drone_commands.height_command import HeightCommand
from drone_commands.land_command import LandCommand
from drone_commands.takeoff_command import TakeoffCommand


class AutoTestCommand(SequentialCommand):

    def __init__(self, drone: Drone):
        super().__init__(
            TakeoffCommand(drone),
            HeightCommand(drone, 100, True),
            LandCommand(drone)
        )
