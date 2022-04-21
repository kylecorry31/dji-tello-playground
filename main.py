import sys

import cv2

from drone.drone import Drone
from drone_commands import *
from controller.xbox_controller import *
from drone_commands.emergency_command import EmergencyCommand
from drone_commands.sensor_update_command import SensorUpdateCommand
from drone_commands.toggle_altitude_hold_command import ToggleAltitudeHoldCommand
from drone_commands.toggle_headless_command import ToggleHeadlessCommand
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
    c = XboxController(0)

    """
    A (press): Liftoff / Land
    B (press): Rotate 90
    Y (press): Throw and go
    X: Nothing
    LS (press): Toggle headless
    RS (hold): Fast mode
    RS (y): Forward / backward
    RS (x): Left / right
    LS (x): Rotate
    START (hold): Alt mode
    BACK (press): Stop
    BACK (double press): Emergency stop
    LB (hold): Hover 100 cm
    RB (press): Toggle altitude hold
    
    Alt:
        UP (press): Flip forward
        DOWN (press): Flip backward
        LEFT (press): Flip left
        RIGHT (press): Flip right
        
    
    """

    def is_alt_mode():
        return c.get_button(START)

    c.when_pressed(A, ToggleFlightCommand(drone))
    c.when_pressed(Y, TakeoffCommand(drone, True))
    c.when_pressed(B, RotateCommand(drone, 90))
    c.when_pressed(DPAD_UP, ConditionalCommand(FlipCommand(drone, FlipFront), None, is_alt_mode))
    c.when_pressed(DPAD_DOWN, ConditionalCommand(FlipCommand(drone, FlipBack), None, is_alt_mode))
    c.when_pressed(DPAD_LEFT, ConditionalCommand(FlipCommand(drone, FlipLeft), None, is_alt_mode))
    c.when_pressed(DPAD_RIGHT, ConditionalCommand(FlipCommand(drone, FlipRight), None, is_alt_mode))
    c.when_pressed(LEFT_THUMB, ToggleHeadlessCommand(drone))
    c.while_held(LB, HeightCommand(drone, 100, False))
    c.when_pressed(RB, ToggleAltitudeHoldCommand(drone))
    c.when_pressed(BACK, EmergencyCommand(drone))
    runner.set_default_command(FlyCommand(drone, c))

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
