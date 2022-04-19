from drone.advanced.tello import Tello
from drone.sensors.sensor import Sensor


class TOF(Sensor):

    def __init__(self, tello: Tello):
        self.tello = tello

    def read(self):
        return self.tello.get_distance_tof()
