import sys

import cv2

from drone.drone import Drone
from drone_commands import *
from controller.xbox_controller import *
from drone_commands.emergency_command import EmergencyCommand
from drone_commands.sensor_update_command import SensorUpdateCommand
from drone_commands.value_display_command import ValueDisplayCommand
from drone.advanced.flips import *


def exception_handler(exctype, value, tb):
    print('Type:', exctype)
    print('Value:', value)
    print('Traceback:', tb)


sys.excepthook = exception_handler

drone = Drone()
runner = CommandRunner.get_instance()


def init():
    runner.schedule(ShowVideoCommand(drone))
    runner.schedule(ValueDisplayCommand(drone))
    runner.schedule(SensorUpdateCommand(drone))


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
    controller.when_pressed(X, TakeoffCommand(drone, True))
    controller.when_pressed(B, RotateCommand(drone, 90))
    controller.when_pressed(LEFT_THUMB, ResetHeadingCommand(drone))
    controller.when_pressed(DPAD_UP, FlipCommand(drone, FlipFront))
    controller.when_pressed(DPAD_DOWN, FlipCommand(drone, FlipBack))
    controller.when_pressed(DPAD_LEFT, FlipCommand(drone, FlipLeft))
    controller.when_pressed(DPAD_RIGHT, FlipCommand(drone, FlipRight))
    height = HeightCommand(drone, 121.9, False)
    controller.while_held(LB, height)
    controller.when_pressed(BACK, EmergencyCommand(drone))
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
