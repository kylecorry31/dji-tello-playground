import time

from commands import Command
from drone.drone import Drone


class EmergencyCommand(Command):
    def __init__(self, drone: Drone):
        super().__init__(drone)
        self.drone = drone
        self.last_activate = None

    def initialize(self):
        self.drone.stop()
        if self.last_activate is None:
            self.last_activate = time.time()
            return
        if time.time() - self.last_activate < 1:
            self.drone.emergency_stop()
        self.last_activate = time.time()

    def is_finished(self):
        return True
