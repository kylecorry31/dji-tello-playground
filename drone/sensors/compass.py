from drone.advanced.tello_sdk import TelloSDK
from drone.sensors.sensor import Sensor
from utils import delta_angle


class Compass(Sensor):
    def __init__(self, tello: TelloSDK):
        self.tello = tello
        self.yaw = None
        self.last_yaw = 0

    def reset(self):
        self.last_yaw = self.tello.get_state().yaw
        self.yaw = 0

    def update(self):
        if self.yaw is None:
            self.reset()
        current_yaw = self.tello.get_state().yaw
        if current_yaw < 0:
            current_yaw += 360
        delta = delta_angle(self.last_yaw, current_yaw)
        self.last_yaw = current_yaw
        self.yaw += delta

    def read(self):
        return self.yaw
