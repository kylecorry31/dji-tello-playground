import logging

from drone.advanced.tello import Tello
from drone.sensors.accelerometer import Accelerometer
from drone.sensors.barometer import Barometer
from drone.sensors.compass import Compass
from drone.sensors.flight_time import FlightTime
from drone.sensors.fused_altimeter import FusedAltimeter
from drone.sensors.mvo import MVO
from drone.sensors.mvo_position_sensor import MVOPositionSensor
from drone.sensors.tof import TOF
from utils import rotate


class Drone:
    def __init__(self):
        self.tello = Tello()
        self.tello.LOGGER.setLevel(logging.ERROR)
        self.tello.connect()
        self.start_height = 0
        self.barometer = Barometer(self.tello)
        self.accelerometer = Accelerometer(self.tello)
        self.mvo = MVO(self.tello)
        self.tof = TOF(self.tello)
        self.flight_time = FlightTime(self.tello)
        self.compass = Compass(self.tello)
        self.position = MVOPositionSensor(self.mvo, self.compass)
        self.altimeter = FusedAltimeter(self.tof, self.barometer, self.mvo, self.accelerometer, self.flight_time)
        print(self.tello.get_battery())
        print("READY")

    def reset_sensors(self):
        self.compass.reset()
        self.flight_time.reset()
        self.barometer.reset()
        self.accelerometer.reset()
        self.mvo.reset()
        self.tof.reset()
        self.altimeter.reset()
        self.position.reset()

    def update_sensors(self):
        self.compass.update()
        self.flight_time.update()
        self.barometer.update()
        self.accelerometer.update()
        self.mvo.update()
        self.tof.update()
        self.altimeter.update()
        self.position.update()

    def stream(self):
        self.tello.streamon()

    def land(self):
        self.tello.land()

    def takeoff(self):
        self.tello.remove_altitude_limit()
        self.tello.send_command_without_return("takeoff")
        self.tello.is_flying = True

    def flip_forward(self):
        self.tello.flip_forward()

    def flip_back(self):
        self.tello.flip_back()

    def flip_right(self):
        self.tello.flip_right()

    def flip_left(self):
        self.tello.flip_left()

    def flip_forwardleft(self):
        self.tello.flip_forwardleft()

    def flip_backleft(self):
        self.tello.flip_backleft()

    def flip_forwardright(self):
        self.tello.flip_forwardright()

    def flip_backright(self):
        self.tello.flip_backright()

    def stop(self):
        self.fly(0, 0, 0, 0)

    def fly(self, x, y, z, yaw, field_oriented=False, fast_mode=False):
        if field_oriented:
            rotated = rotate((x, y), self.get_yaw())
            x = rotated[0]
            y = rotated[1]
        self.tello.send_rc_control(int(x * 100), int(y * 100), int(z * 100), int(yaw * 100), fast_mode)

    def disconnect(self):
        self.tello.end()

    def get_video(self):
        return self.tello.get_video_capture()

    def get_frame(self):
        return self.tello.get_frame_read().frame

    def get_battery(self):
        return self.tello.get_battery()

    def get_height_from_ground(self):
        return self.altimeter.read()

    def get_height_from_start(self):
        if self.start_height == 0:
            self.start_height = self.barometer.read()
        return self.barometer.read() - self.start_height

    def get_height(self):
        # TODO: Remove this
        return self.tello.get_height()

    def emergency_stop(self):
        self.tello.emergency()

    def get_yaw(self):
        return self.compass.read()

    def is_flying(self):
        flying = self.get_height() != 0
        self.tello.is_flying = flying
        return flying

    def fly_to(self, x, y, z, speed):
        self.tello.go_xyz_speed(int(x), int(y), int(z), int(speed * 100))

    def rotate(self, yaw):
        if yaw < 0:
            self.tello.rotate_counter_clockwise(-int(yaw))
        else:
            self.tello.rotate_clockwise(int(yaw))

    def reset_heading(self):
        self.compass.reset()
