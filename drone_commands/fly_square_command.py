from commands import SequentialCommand
from drone.drone import Drone
from drone_commands.fly_to_command import FlyToCommand
from drone_commands.land_command import LandCommand
from drone_commands.takeoff_command import TakeoffCommand


class AutoFlySquareCommand(SequentialCommand):

    def __init__(self, drone: Drone):
        super().__init__(
            TakeoffCommand(drone),
            FlyToCommand(drone, 0, 50, 0, 50),
            FlyToCommand(drone, 50, 0, 0, 50),
            FlyToCommand(drone, 0, -50, 0, 50),
            FlyToCommand(drone, -50, 0, 0, 50),
            LandCommand(drone)
        )
