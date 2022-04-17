from commands.command import Command
from drone.drone import Drone


class LandCommand(Command):

    def __init__(self, drone: Drone):
        super().__init__(drone)
        self.drone = drone

    def execute(self):
        self.drone.fly(0, 0, -1, 0)

    def is_finished(self):
        return not self.drone.is_flying()

    def end(self, interrupted):
        if not interrupted:
            self.drone.land()
        self.drone.stop()
