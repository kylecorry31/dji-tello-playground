from drone.modules.fly_module import FlyModule


class SpeedLimitModule(FlyModule):
    def __init__(self, max_speed: float, fast_mode_allowed: bool):
        super().__init__()
        self.max_speed = max_speed
        self.fast_mode_allowed = fast_mode_allowed

    def run(self, x: float, y: float, z: float, yaw: float, fast_mode: bool) -> (float, float, float, float, bool):
        return x * self.max_speed, y * self.max_speed, z * self.max_speed, yaw * self.max_speed, fast_mode and self.fast_mode_allowed
