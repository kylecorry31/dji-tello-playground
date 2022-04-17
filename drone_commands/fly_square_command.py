from commands import SequentialCommand, ParallelRaceCommand, WaitCommand
from drone.drone import Drone
from drone_commands.rotate_command import RotateCommand
from drone_commands.fly_to_command import FlyToCommand
from drone_commands.land_command import LandCommand
from drone_commands.takeoff_command import TakeoffCommand


class AutoFlySquareCommand(SequentialCommand):

    def __init__(self, drone: Drone):
        super().__init__(
            TakeoffCommand(drone),
            RotateCommand(drone, -90),
            # FlyToCommand(drone, 0, 50, 0, 50),
            # FlyToCommand(drone, 50, 0, 0, 50),
            # FlyToCommand(drone, 0, -50, 0, 50),
            # FlyToCommand(drone, -50, 0, 0, 50),
            LandCommand(drone)
        )
