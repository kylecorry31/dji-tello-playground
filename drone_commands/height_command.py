from commands.PIDCommand import PIDCommand
from drone.tello import Tello
from filter.pid import PID


class HeightCommand(PIDCommand):

    def __init__(self, drone: Tello, height: float, relative=True):
        pid = PID(0.05, 0.01, 0.15)
        pid.position_tolerance = 1
        pid.integrator_range = 10
        pid.integrator_limit = 0.25
        super().__init__(drone, self.get_height, self.set_velocity, height, pid=pid, relative=relative,
                         timeout_fn=self.estimate_time)
        self.drone = drone
        self.relative = relative

    def set_velocity(self, velocity):
        self.drone.fly(0, 0, velocity, 0)

    def estimate_time(self, error):
        return abs(error) / 65

    def get_height(self):
        return self.drone.altimeter.read()
