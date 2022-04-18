import numpy as np
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter

from commands import Command
from drone.drone import Drone


class HeightEstimationCommand(Command):
    def __init__(self, drone: Drone):
        super().__init__(None)
        self.drone = drone
        self.height = 0
        self.filter = KalmanFilter(dim_x=2, dim_z=1)
        self.last_baro = None
        self.last_tof = None

    def initialize(self):
        # self.filter.x = np.array([[0.], [0.]])
        # self.filter.F = np.array([[1., 1.], [0., 1.]])
        # self.filter.H = np.array([[1., 0.]])
        # self.filter.P *= 1000.
        # self.filter.R = 50.
        # self.filter.Q *= 0
        self.drone.start_height = 0
        self.last_baro = self.drone.get_barometer()
        self.last_tof = self.drone.get_tof()
        if self.is_tof_valid(self.last_tof):
            self.height = self.last_tof
        else:
            self.height = 0
        self.drone.h = self.height

    def is_tof_valid(self, tof):
        return tof > 10 and tof < 6553

    def execute(self):
        tof = self.drone.get_tof()
        baro = self.drone.get_barometer()
        d_baro = baro - self.last_baro
        self.last_baro = baro

        if self.is_tof_valid(tof):
            self.height = tof
        else:
            self.height += d_baro

        self.drone.h = max(0., self.height)

    def is_finished(self):
        return False