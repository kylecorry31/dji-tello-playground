import sys

import cv2

from drone.drone import Drone
from drone_commands import *
from controller.xbox_controller import *


def exception_handler(exctype, value, tb):
    print('Type:', exctype)
    print('Value:', value)
    print('Traceback:', tb)


sys.excepthook = exception_handler

drone = Drone()
runner = CommandRunner.get_instance()


def init():
    runner.schedule(ShowVideoCommand(drone))


def autonomous():
    runner.schedule(AutoTestCommand(drone))
    while True:
        try:
            runner.update()
            time.sleep(0.01)
        except KeyboardInterrupt:
            break
        except Exception:
            pass


def teleop():
    controller = XboxController(0)
    controller.when_pressed(A, ToggleFlightCommand(drone))
    controller.when_pressed(X, RotateCommand(drone, -90))
    controller.when_pressed(B, RotateCommand(drone, 90))
    controller.when_pressed(DPAD_DOWN, ResetHeadingCommand(drone))
    height = HeightCommand(drone, 100, False)
    controller.when_pressed(LB, height)
    controller.when_released(LB, CancelCommand(height))
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


def end():
    runner.cancel_all(True)
    drone.disconnect()
    cv2.destroyAllWindows()


init()
# autonomous()
teleop()
end()
