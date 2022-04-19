import sys

import cv2

from drone.simple_drone import SimpleDrone
from drone_commands import *
from controller.xbox_controller import *

drone = SimpleDrone()
runner = CommandRunner.get_instance()


def teleop():
    controller = XboxController(0)
    controller.when_pressed(A, ToggleFlightCommand(drone))
    controller.while_held(START, StopCommand(drone))
    runner.set_default_command(FlyCommand(drone, controller))

    while True:
        try:
            runner.update()
            time.sleep(0.01)
        except KeyboardInterrupt:
            break
        except Exception:
            pass


teleop()
