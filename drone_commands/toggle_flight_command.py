from commands import ConditionalCommand
from drone.drone import Drone

from drone_commands.land_command import LandCommand
from drone_commands.takeoff_command import TakeoffCommand


class ToggleFlightCommand(ConditionalCommand):

    def __init__(self, drone: Drone):
        super().__init__(LandCommand(drone), TakeoffCommand(drone), lambda: drone.is_flying())
