class FlyModule:

    def __init__(self):
        self.is_enabled = True

    def run(self, x: float, y: float, z: float, yaw: float, fast_mode: bool) -> (float, float, float, float, bool):
        return x, y, z, yaw, fast_mode

    def reset(self):
        pass