from commands.PIDCommand import PIDCommand
from drone.drone import Drone
from utils import delta_angle


class RotateCommand(PIDCommand):

    def __init__(self, drone: Drone, yaw: float, relative=True):
        super().__init__(drone, self.get_yaw, self.set_velocity, yaw, p=0.05, threshold=1, relative=relative,
                         timeout_fn=self.estimate_time, error_fn=self.calculate_error)
        self.drone = drone
        self.relative = relative

    def set_velocity(self, velocity):
        self.drone.fly(0, 0, 0, velocity)

    def estimate_time(self, error):
        return abs(error) / 65

    def get_yaw(self):
        return self.drone.get_yaw()

    def calculate_error(self, target, current):
        if self.relative:
            return target - current
        return delta_angle(current, target)
