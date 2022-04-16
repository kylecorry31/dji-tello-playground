from commands.command import Command
from drone.drone import Drone


class RotateCommand(Command):

    def __init__(self, drone: Drone, yaw: float):
        super().__init__(drone)
        self.drone = drone
        # self.start_time = None
        self.yaw = yaw
        self.start_yaw = None
        # self.estimated_time = yaw / 50

    def initialize(self):
        self.start_yaw = self.drone.get_yaw()
        self.drone.rotate(self.yaw)
        # self.start_time = time.time()

    def is_finished(self):
        return abs(self.drone.get_yaw() - self.start_yaw) >= abs(self.yaw)
        # return time.time() - self.start_time > self.estimated_time

    def end(self, interrupted):
        self.drone.stop()
