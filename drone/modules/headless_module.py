from drone.modules.fly_module import FlyModule
from drone.sensors.compass import Compass
from utils import rotate


class HeadlessModule(FlyModule):
    def __init__(self, compass: Compass):
        super().__init__()
        self.compass = compass

    def reset(self):
        self.compass.reset()

    def run(self, x: float, y: float, z: float, yaw: float, fast_mode: bool) -> (float, float, float, float, bool):
        rotated = rotate((x, y), self.compass.read())
        x = rotated[0]
        y = rotated[1]
        return x, y, z, yaw, fast_mode
