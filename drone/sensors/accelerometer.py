from drone.advanced.tello import Tello
from drone.sensors.sensor import Sensor


class Accelerometer(Sensor):
    def __init__(self, tello: Tello):
        self.tello = tello

    def read(self):
        return self.tello.get_acceleration_x(), self.tello.get_acceleration_y(), self.tello.get_acceleration_z()
