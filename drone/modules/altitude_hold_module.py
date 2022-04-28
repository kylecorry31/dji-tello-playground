import time

from drone.modules.fly_module import FlyModule
from drone.sensors.fused_altimeter import FusedAltimeter
from filter.pid import PID


class AltitudeHoldModule(FlyModule):
    def __init__(self, altimeter: FusedAltimeter, pid: PID):
        super().__init__()
        self.altimeter = altimeter
        self.maintain_pid = pid
        self.last_time = time.time()
        self.maintain_height = None

    def reset(self):
        self.maintain_height = None
        self.maintain_pid.reset()
        self.last_time = time.time()

    def run(self, x: float, y: float, z: float, yaw: float, fast_mode: bool) -> (float, float, float, float, bool):
        return x, y, self.__get_z(z), yaw, fast_mode

    def __can_run(self, altitude: float) -> bool:
        return 10 < altitude < 1000

    def __get_z(self, user):
        dt = time.time() - self.last_time
        self.last_time = time.time()

        # If the user is not moving, maintain the height
        if abs(user) < 0.1 and self.maintain_height is not None and self.__can_run(self.altimeter.read()):
            return self.maintain_pid.calculate(self.altimeter.read(), self.maintain_height, dt)

        # If the user is moving up/down, set the new maintain height
        self.maintain_height = self.altimeter.read()

        # Don't maintain height if it is too high or low
        if not self.__can_run(self.maintain_height):
            self.maintain_height = None

        return user
