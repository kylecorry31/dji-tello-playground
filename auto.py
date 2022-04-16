import cv2

from drone_commands import *
from controller.xbox_controller import *
from drone.fake_drone import FakeDrone

drone = FakeDrone()
runner = CommandRunner.get_instance()
runner.schedule(ShowVideoCommand(drone))
runner.schedule(AutoFlySquareCommand(drone))

while True:
    try:
        runner.update()
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
    except KeyboardInterrupt:
        break

runner.cancel_all()
drone.disconnect()
cv2.destroyAllWindows()
