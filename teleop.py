import cv2

from drone.drone import Drone
from drone_commands import *
from controller.xbox_controller import *

drone = Drone()
runner = CommandRunner.get_instance()
controller = XboxController(0)
controller.when_pressed(A, ToggleFlightCommand(drone))
controller.while_held(START, StopCommand(drone))
runner.set_default_command(FlyCommand(drone, controller))
runner.schedule(ShowVideoCommand(drone))

while True:
    try:
        runner.update()
    except KeyboardInterrupt:
        break
    except Exception:
        pass

runner.cancel_all()
drone.disconnect()
cv2.destroyAllWindows()
