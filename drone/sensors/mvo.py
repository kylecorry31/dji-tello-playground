from drone.advanced.tello_sdk import TelloSDK
from drone.sensors.sensor import Sensor


class MVO(Sensor):

    def __init__(self, tello: TelloSDK):
        self.tello = tello

    def read(self):
        state = self.tello.get_state()
        return state.vgx * 10, state.vgy * 10, state.vgz * 10
