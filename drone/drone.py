import time

from drone.advanced.tello_sdk import TelloSDK
from drone.modules.altitude_hold_module import AltitudeHoldModule
from drone.modules.headless_module import HeadlessModule
from drone.modules.speed_limit_module import SpeedLimitModule
from drone.sensors.accelerometer import Accelerometer
from drone.sensors.barometer import Barometer
from drone.sensors.compass import Compass
from drone.sensors.flight_time import FlightTime
from drone.sensors.fused_altimeter import FusedAltimeter
from drone.sensors.mvo import MVO
from drone.sensors.mvo_position_sensor import MVOPositionSensor
from drone.sensors.tof import TOF


class Drone:
    def __init__(self):
        self.tello = TelloSDK(print_responses=False)
        self.tello.command()
        self.tello.set_stream(True)
        self.tello.set_altitude_limit(30)
        self.__was_fast_mode = False
        while not self.tello.has_valid_state():
            time.sleep(0.1)
        self.barometer = Barometer(self.tello)
        self.accelerometer = Accelerometer(self.tello)
        self.mvo = MVO(self.tello)
        self.tof = TOF(self.tello)
        self.flight_time = FlightTime(self.tello)
        self.compass = Compass(self.tello)
        self.position = MVOPositionSensor(self.mvo, self.compass)
        self.altimeter = FusedAltimeter(self.tof, self.barometer, self.mvo, self.accelerometer, self.flight_time)

        # Set up modules
        self.headless_module = HeadlessModule(self.compass)
        self.headless_module.is_enabled = False
        self.altitude_hold_module = AltitudeHoldModule(self.altimeter)
        self.altitude_hold_module.is_enabled = False
        self.speed_limit_module = SpeedLimitModule(1.0, True)
        self.modules = [self.headless_module, self.altitude_hold_module, self.speed_limit_module]

        print("READY")

    def get_wifi(self, callback=None):
        return self.tello.read_wifi(callback)

    def get_battery(self):
        return self.tello.get_state().bat

    def reset_sensors(self):
        self.compass.reset()
        self.flight_time.reset()
        self.barometer.reset()
        self.accelerometer.reset()
        self.mvo.reset()
        self.tof.reset()
        self.altimeter.reset()
        self.position.reset()
        for module in self.modules:
            module.reset()

    def update_sensors(self):
        self.compass.update()
        self.flight_time.update()
        self.barometer.update()
        self.accelerometer.update()
        self.mvo.update()
        self.tof.update()
        self.altimeter.update()
        self.position.update()

    def land(self, palm: bool = False):
        if palm:
            self.tello.palm_land()
        else:
            self.tello.land()

    def takeoff(self, throw: bool = False):
        if throw:
            self.tello.throw_and_go()
        else:
            self.tello.takeoff(True)

    def is_flying(self):
        return self.tello.get_state().h != 0

    def stop(self):
        self.fly(0, 0, 0, 0)

    def disconnect(self):
        self.tello.disconnect()

    def fly(self, x, y, z, yaw, fast_mode=False, run_modules=False):
        if run_modules:
            for module in self.modules:
                if module.is_enabled:
                    (x, y, z, yaw, fast_mode) = module.run(x, y, z, yaw, fast_mode)
        if fast_mode or self.__was_fast_mode:
            self.tello.stick(x, y, z, yaw, fast_mode)
        else:
            self.tello.rc(x, y, z, yaw)
        self.__was_fast_mode = fast_mode

    def go(self, x, y, z, speed, listener=None):
        self.tello.go(x, y, z, speed, listener)

    def emergency_stop(self):
        self.tello.emergency()

    def flip(self, direction: int):
        self.tello.flip(direction)
