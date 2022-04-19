from commands.command import Command
from drone.drone import Drone


class TakeoffCommand(Command):

    def __init__(self, drone: Drone):
        super().__init__(drone)
        self.drone = drone

    def initialize(self):
        if self.is_finished():
            return
        self.drone.start_height = 0
        self.drone.takeoff()

    def is_finished(self):
        return self.drone.is_flying()

    def end(self, interrupted):
        if interrupted:
            self.drone.stop()
