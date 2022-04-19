import time

from commands import Command
from drone.drone import Drone
from utils import rotate


class ValueDisplayCommand(Command):
    def __init__(self, drone: Drone):
        super().__init__(None)
        self.drone = drone
        self.last_time = None
        self.last_execute = None
        self.position = (0, 0, 0)

    def initialize(self):
        self.position = (0, 0, 0)
        self.last_execute = None

    def execute(self):
        if self.last_execute is not None:
            dt = time.time() - self.last_execute
            speed = self.drone.mvo.read()
            if speed is not None:
                (x_speed, y_speed) = rotate((speed[0], speed[1]), self.drone.get_yaw())
                self.position = (
                    self.position[0] + x_speed * dt,
                    self.position[1] + y_speed * dt,
                    self.drone.get_height_from_start()
                )
                self.last_execute = time.time()
        else:
            self.last_execute = time.time()

        if self.last_time is None or time.time() - self.last_time > 0.1:
            self.last_time = time.time()
            pos = (int(self.position[0]), int(self.position[1]), int(self.position[2]))
            print("Time:", self.drone.flight_time.read(), "Height:", int(self.drone.get_height_from_ground()), "Bat:",
                  self.drone.get_battery())

    def is_finished(self):
        return False
