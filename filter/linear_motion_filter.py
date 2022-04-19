import time

from filter.linear_combination_filter import LinearCombinationFilter


class LinearMotionFilter:

    def __init__(self, position_weight, velocity_weight, acceleration_weight):
        self.combination = LinearCombinationFilter([position_weight, velocity_weight, acceleration_weight])
        self.last_position = 0
        self.last_time = 0

    def adjust_weights(self, position_weight, velocity_weight, acceleration_weight):
        self.combination.weights = [position_weight, velocity_weight, acceleration_weight]

    def calculate(self, position, velocity, acceleration):
        if self.last_time == 0:
            self.last_position = position
            self.last_time = time.time()
            return

        dt = time.time() - self.last_time
        self.last_time = time.time()
        self.last_position = self.combination.calculate(
            [position, self.last_position + velocity * dt, self.last_position + 0.5 * acceleration * dt * dt])
        return self.last_position
