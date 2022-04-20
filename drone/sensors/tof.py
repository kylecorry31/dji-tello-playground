from drone.advanced.tello_sdk import TelloSDK
from drone.sensors.sensor import Sensor


class TOF(Sensor):

    def __init__(self, tello: TelloSDK):
        self.tello = tello

    def read(self):
        return self.tello.get_state().tof
