from controller.xbox_controller import *
from drone.tello import Tello
from drone_commands import *
from drone_commands.emergency_command import EmergencyCommand

drone = Tello()
runner = CommandRunner.get_instance()
runner.schedule(ShowVideoCommand(drone))


def teleop():
    controller = XboxController(0)
    controller.when_pressed(A, ToggleFlightCommand(drone))
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


teleop()
