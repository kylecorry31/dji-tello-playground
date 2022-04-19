from drone.advanced.tello import Tello
from drone.sensors.sensor import Sensor
from filter.linear_combination_filter import LinearCombinationFilter


class Barometer(Sensor):
    def __init__(self, tello: Tello, alpha=0.9):
        self.filter = LinearCombinationFilter([alpha, 1 - alpha])
        self.last_value = 0
        self.tello = tello

    def read(self):
        return self.last_value

    def update(self):
        if self.last_value == 0:
            self.last_value = self.tello.get_barometer()
        self.last_value = self.filter.calculate([self.last_value, self.tello.get_barometer()])
