from commands.PIDCommand import PIDCommand
from drone.drone import Drone


class HeightCommand(PIDCommand):

    def __init__(self, drone: Drone, height: float, relative=True):
        super().__init__(drone, self.get_height, self.set_velocity, height, p=0.05, threshold=2, relative=relative,
                         timeout_fn=self.estimate_time)
        self.drone = drone
        self.relative = relative

    def set_velocity(self, velocity):
        self.drone.fly(0, 0, velocity, 0)

    def estimate_time(self, error):
        return abs(error) / 65

    def get_height(self):
        return self.drone.get_tof() if not self.relative else self.drone.get_height()
