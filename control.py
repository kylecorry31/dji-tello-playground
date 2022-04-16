import cv2

from commands import SequentialCommand
from drone_commands import *
from controller.xbox_controller import *
from drone.fake_drone import FakeDrone

drone = FakeDrone()
runner = CommandRunner.get_instance()
controller = XboxController(0)
controller.when_pressed(Y, SequentialCommand(FlipLeftCommand(drone), FlipRightCommand(drone)))
controller.when_pressed(X, FlipLeftCommand(drone))
controller.when_pressed(B, FlipRightCommand(drone))
controller.when_pressed(A, ToggleFlightCommand(drone))
controller.when_pressed(START, StopCommand(drone))
runner.set_default_command(FlyCommand(drone, controller))
runner.schedule(ShowVideoCommand(drone))

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
