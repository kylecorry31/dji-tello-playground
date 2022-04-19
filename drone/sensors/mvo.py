from drone.advanced.tello import Tello
from drone.sensors.sensor import Sensor


class MVO(Sensor):

    def __init__(self, tello: Tello):
        self.tello = tello

    def read(self):
        return self.tello.get_speed_x() * 10, self.tello.get_speed_y() * 10, self.tello.get_speed_z() * 10
