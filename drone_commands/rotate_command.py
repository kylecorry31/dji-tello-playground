from commands.PIDCommand import PIDCommand
from drone.drone import Drone
from filter.pid import PID
from utils import delta_angle


class RotateCommand(PIDCommand):

    def __init__(self, drone: Drone, yaw: float, relative=True):
        pid = PID(0.05, 0, 0)
        pid.position_tolerance = 1
        pid.error_fn = self.calculate_error
        super().__init__(drone, self.get_yaw, self.set_velocity, yaw, pid=pid, relative=relative,
                         timeout_fn=self.estimate_time)
        self.drone = drone
        self.relative = relative

    def set_velocity(self, velocity):
        self.drone.fly(0, 0, 0, velocity)

    def estimate_time(self, error):
        return abs(error) / 65

    def get_yaw(self):
        return self.drone.compass.read()

    def calculate_error(self, target, current):
        if self.relative:
            return target - current
        return delta_angle(current, target)
