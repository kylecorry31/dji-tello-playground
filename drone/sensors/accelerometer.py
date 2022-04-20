from drone.advanced.tello_sdk import TelloSDK
from drone.sensors.sensor import Sensor


class Accelerometer(Sensor):
    def __init__(self, tello: TelloSDK):
        self.tello = tello

    def read(self):
        state = self.tello.get_state()
        return state.agx, state.agy, state.agz
