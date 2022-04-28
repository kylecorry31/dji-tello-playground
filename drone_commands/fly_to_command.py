import math

from commands.command import Command
import time

from drone.tello import Tello


class FlyToCommand(Command):

    def __init__(self, drone: Tello, x: float, y: float, z: float, speed: float):
        super().__init__(drone)
        self.drone = drone
        self.start_time = None
        self.x = x
        self.y = y
        self.z = z
        self.speed = speed
        distance = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        self.estimated_time = distance / (speed * 100)

    def initialize(self):
        self.drone.go(self.x, self.y, self.z, self.speed)
        self.start_time = time.time()

    def is_finished(self):
        return time.time() - self.start_time > self.estimated_time

    def end(self, interrupted):
        self.drone.stop()
