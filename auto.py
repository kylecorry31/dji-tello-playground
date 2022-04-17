import cv2

from drone.drone import Drone
from drone_commands import *
from controller.xbox_controller import *

drone = Drone()
runner = CommandRunner.get_instance()
# runner.schedule(ShowVideoCommand(drone))
runner.schedule(AutoFlySquareCommand(drone))

while True:
    try:
        runner.update()
        time.sleep(0.01)
    except KeyboardInterrupt:
        break

runner.cancel_all(True)
drone.disconnect()
cv2.destroyAllWindows()
