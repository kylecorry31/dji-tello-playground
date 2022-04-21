from drone.modules.fly_module import FlyModule
from drone.sensors.compass import Compass
from utils import rotate


class HeadlessModule(FlyModule):
    def __init__(self, compass: Compass):
        super().__init__()
        self.compass = compass
        self.forward_yaw = compass.read()

    def reset(self):
        self.forward_yaw = self.compass.read()

    def run(self, x: float, y: float, z: float, yaw: float, fast_mode: bool) -> (float, float, float, float, bool):
        rotated = rotate((x, y), self.compass.read() - self.forward_yaw)
        x = rotated[0]
        y = rotated[1]
        return x, y, z, yaw, fast_mode
