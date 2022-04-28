from commands.command import Command
from drone.tello import Tello


class TakeoffCommand(Command):

    def __init__(self, drone: Tello, throw: bool = False):
        super().__init__(drone)
        self.drone = drone
        self.throw = throw

    def initialize(self):
        self.drone.takeoff(self.throw)

    def is_finished(self):
        return self.drone.is_flying()

    def end(self, interrupted):
        if interrupted:
            self.drone.stop()
