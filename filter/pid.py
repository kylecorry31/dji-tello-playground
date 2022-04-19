import math

from utils import clamp


class PID:

    def __init__(self, p: float, i: float, d: float, error_fn=None):
        self.p = p
        self.i = i
        self.d = d
        self.position_tolerance = 0.05
        self.velocity_tolerance = math.inf
        self.integrator_limit = math.inf
        self.integrator_range = math.inf
        self.position_error = None
        self.velocity_error = None
        self.total_error = 0.0
        if error_fn is not None:
            self.error_fn = error_fn
        else:
            self.error_fn = self.__default_error_fn

    def __default_error_fn(self, target, current):
        return target - current

    def calculate(self, current: float, target: float, dt: float) -> float:
        last_error = self.position_error
        self.position_error = self.error_fn(target, current)
        d_term = 0.0

        if last_error is not None:
            self.velocity_error = (self.position_error - last_error) / dt
            d_term = self.velocity_error * self.d

        if self.i != 0.0:
            self.total_error = clamp(self.total_error + self.position_error * dt, -self.integrator_limit,
                                     self.integrator_limit)
            if abs(self.position_error) >= self.integrator_range:
                self.total_error = 0

        return self.p * self.position_error + self.i * self.total_error + d_term

    def at_setpoint(self) -> bool:
        if self.velocity_error is None:
            return False
        return abs(self.position_error) <= self.position_tolerance and abs(
            self.velocity_error) <= self.velocity_tolerance

    def reset(self):
        self.position_error = None
        self.velocity_error = None
        self.total_error = 0.0
