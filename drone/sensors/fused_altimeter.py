from drone.sensors.barometer import Barometer
from drone.sensors.accelerometer import Accelerometer
from drone.sensors.flight_time import FlightTime
from drone.sensors.mvo import MVO
from drone.sensors.sensor import Sensor
from drone.sensors.tof import TOF
from filter.linear_motion_filter import LinearMotionFilter


class FusedAltimeter(Sensor):
    def __init__(self, tof: TOF, barometer: Barometer, mvo: MVO, accelerometer: Accelerometer, flight_time: FlightTime):
        self.accelerometer = accelerometer
        self.mvo = mvo
        self.barometer = barometer
        self.tof = tof
        self.flight_time = flight_time
        self.filter = LinearMotionFilter(0.7, 0.2, 0.1)
        self.baseline_baro = None
        self.stationary_count = 0
        self.height = 0

    def is_tof_valid(self, tof):
        # TODO: Move this to the sensor
        return tof > 10 and tof < 6553

    def reset(self):
        tof = self.tof.read()
        if self.is_tof_valid(tof):
            height = tof
        else:
            height = 0
        self.baseline_baro = self.barometer.read() - height
        self.filter.last_position = height

    def update(self):
        if self.baseline_baro is None:
            self.reset()

        pos = self.tof.read()
        baro = self.barometer.read()
        vel = -self.mvo.read()[2]
        motion = self.accelerometer.read()
        acc = motion[2] + 1000

        if self.baseline_baro == 0:
            self.baseline_baro = baro
            return

        if not self.is_tof_valid(pos):
            self.filter.adjust_weights(0.5, 0.4, 0.1)
            pos = baro - self.baseline_baro
        else:
            self.filter.adjust_weights(0.7, 0.2, 0.1)
            self.baseline_baro = self.barometer.read() - pos

        if self.flight_time.read() == 0:
            # Drone is stationary, which means it is on the ground
            pos = 0
            self.baseline_baro = self.barometer.read()

        self.filter.calculate(pos, vel, acc)

    def read(self):
        return max(0, self.filter.last_position)
