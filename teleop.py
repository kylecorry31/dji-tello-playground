import cv2

from drone.drone import Drone
from drone_commands import *
from controller.xbox_controller import *

drone = Drone()
runner = CommandRunner.get_instance()
controller = XboxController(0)
controller.when_pressed(A, ToggleFlightCommand(drone))
controller.when_pressed(X, RotateCommand(drone, -90))
controller.when_pressed(B, RotateCommand(drone, 90))
controller.while_held(START, StopCommand(drone))
runner.set_default_command(FlyCommand(drone, controller))
runner.schedule(ShowVideoCommand(drone))

while True:
    try:
        runner.update()
        time.sleep(0.01)
    except KeyboardInterrupt:
        break
    except Exception:
        pass

runner.cancel_all(True)
drone.disconnect()
cv2.destroyAllWindows()
