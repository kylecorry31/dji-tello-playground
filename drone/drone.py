import logging

from drone.advanced import protocol
from drone.advanced.protocol import Packet
from drone.advanced.tello import Tello
from utils import delta_angle, rotate


class Drone:
    def __init__(self):
        self.tello = Tello()
        self.tello.LOGGER.setLevel(logging.ERROR)
        self.tello.connect()
        self.yaw = None
        self.last_yaw = 0
        print(self.tello.get_battery())
        print("READY")

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

    def get_height(self):
        return self.tello.get_height()

    def get_tof(self):
        return self.tello.get_distance_tof()

    def get_barometer(self):
        return self.tello.get_barometer()

    def emergency_stop(self):
        self.tello.emergency()

    def get_speed(self):
        return self.tello.get_speed_x(), self.tello.get_speed_y(), self.tello.get_speed_z()

    def get_acceleration(self):
        return self.tello.get_acceleration_x(), self.tello.get_acceleration_y(), self.tello.get_acceleration_z()

    def get_yaw(self):
        if self.yaw is None:
            self.reset_heading()
        current_yaw = self.tello.get_yaw()
        if current_yaw < 0:
            current_yaw += 360
        delta = delta_angle(self.last_yaw, current_yaw)
        self.last_yaw = current_yaw
        self.yaw += delta
        return self.yaw

    def is_flying(self):
        flying = self.get_height() > 0
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
        self.last_yaw = self.tello.get_yaw()
        self.yaw = 0
