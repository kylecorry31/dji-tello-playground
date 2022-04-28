import threading
import time

from drone.advanced.tello_sdk import TelloSDK
from drone.drone import Drone
from drone.modules.altitude_hold_module import AltitudeHoldModule
from drone.modules.headless_module import HeadlessModule
from drone.sensors.accelerometer import Accelerometer
from drone.sensors.barometer import Barometer
from drone.sensors.compass import Compass
from drone.sensors.flight_time import FlightTime
from drone.sensors.fused_altimeter import FusedAltimeter
from drone.sensors.mvo import MVO
from drone.sensors.tof import TOF
from filter.pid import PID
from video.tello_camera import TelloCamera


class Tello(Drone):
    def __init__(self):
        super().__init__()
        self.__tello = TelloSDK(print_responses=False)
        self.__tello.command()
        self.__tello.set_stream(True)
        self.__tello.set_altitude_limit(30)
        self.__is_fast_mode = False
        while not self.__tello.has_valid_state():
            time.sleep(0.1)
        barometer = Barometer(self.__tello)
        accelerometer = Accelerometer(self.__tello)
        mvo = MVO(self.__tello)
        tof = TOF(self.__tello)
        self.__flight_time = FlightTime(self.__tello)
        self.__compass = Compass(self.__tello)
        self.__altimeter = FusedAltimeter(tof, barometer, mvo, accelerometer, self.__flight_time)

        self.__sensors = [
            barometer,
            accelerometer,
            mvo,
            tof,
            self.__flight_time,
            self.__compass,
            self.__altimeter
        ]

        # Set up modules
        self.__headless_module = HeadlessModule(self.__compass)
        self.__headless_module.is_enabled = False
        self.__altitude_hold_module = AltitudeHoldModule(self.__altimeter, PID(0.03, 0.0, 0.05))
        self.__altitude_hold_module.is_enabled = False
        self.__modules = [self.__headless_module, self.__altitude_hold_module]

        self.__camera = TelloCamera()
        self.__camera.start()

        self.__is_running = True
        threading.Thread(target=self.__update, daemon=True).start()

        print("READY")

    def get_battery(self):
        return self.__tello.get_state().bat

    def __update(self):
        while self.__is_running:
            for sensor in self.__sensors:
                sensor.update()
            time.sleep(0.01)

    def land(self):
        self.__tello.land()

    def takeoff(self):
        self.__tello.takeoff(False)

    def is_flying(self):
        return self.__tello.get_state().h != 0

    def __del__(self):
        self.__is_running = False
        self.__camera.stop()
        self.__tello.disconnect()

    def fly(self, x, y, z, yaw, fast_mode=False):
        for module in self.__modules:
            if module.is_enabled:
                (x, y, z, yaw, fast_mode) = module.run(x, y, z, yaw, fast_mode)
        if fast_mode or self.__is_fast_mode:
            self.__tello.stick(x, y, z, yaw, fast_mode)
        else:
            self.__tello.rc(x, y, z, yaw)
        self.__is_fast_mode = fast_mode

    def emergency_stop(self):
        self.__tello.emergency()

    def get_altitude(self) -> float:
        return self.__altimeter.read()

    def get_yaw(self) -> float:
        return self.__compass.read()

    def set_headless(self, is_on: bool):
        if is_on:
            self.__headless_module.reset()
        self.__headless_module.is_enabled = is_on

    def is_headless(self) -> bool:
        return self.__headless_module.is_enabled

    def is_holding_altitude(self) -> bool:
        return self.__altitude_hold_module.is_enabled

    def hold_altitude(self, is_on: bool):
        if is_on:
            self.__altitude_hold_module.reset()
        self.__altitude_hold_module.is_enabled = is_on

    def flip(self, direction: int):
        self.__tello.flip(direction)

    def get_frame(self):
        return self.__camera.get_frame()
