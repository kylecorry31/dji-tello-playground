import time

from drone.sensors.compass import Compass
from drone.sensors.mvo import MVO
from drone.sensors.sensor import Sensor
from utils import rotate


class MVOPositionSensor(Sensor):
    def __init__(self, mvo: MVO, compass: Compass):
        self.mvo = mvo
        self.pos = (0, 0, 0)
        self.compass = compass
        self.last_time = time.time()

    def update(self):
        dt = time.time() - self.last_time
        self.last_time = time.time()
        speed = self.mvo.read()
        if speed is None:
            return
        (speed_y, speed_x) = rotate((speed[1], speed[2]), self.compass.read())
        self.pos = (
            self.pos[0] - speed_x * dt,
            self.pos[1] - speed_y * dt,
            self.pos[2] - speed[2] * dt
        )

    def reset(self):
        self.last_time = time.time()
        self.pos = (0, 0, 0)

    def read(self):
        return self.pos
