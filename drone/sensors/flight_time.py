import time

from drone.advanced.tello_sdk import TelloSDK
from drone.sensors.sensor import Sensor


class FlightTime(Sensor):
    def __init__(self, tello: TelloSDK):
        self.tello = tello
        self.last_flight_time = 0
        self.last_flight_time_change = 0
        self.previous_flight_time = 0

    def reset(self):
        self.previous_flight_time = self.__get_flight_time()

    def read(self):
        return self.__get_flight_time() - self.previous_flight_time

    def update(self):
        t = self.__get_flight_time()
        if t != self.last_flight_time or self.last_flight_time_change == 0:
            self.last_flight_time_change = time.time()

        if t == self.last_flight_time and time.time() - self.last_flight_time_change > 1.5:
            self.previous_flight_time = t

        self.last_flight_time = t

    def __get_flight_time(self):
        return self.tello.get_state().time
