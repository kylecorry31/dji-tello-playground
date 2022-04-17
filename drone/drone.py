import logging

import djitellopy
from djitellopy import Tello


class Drone:
    def __init__(self):
        self.x_velocity = 0
        self.y_velocity = 0
        self.z_velocity = 0
        self.yaw_velocity = 0
        self.tello = djitellopy.Tello()
        self.tello.LOGGER.setLevel(logging.ERROR)
        self.tello.connect()
        print(self.tello.get_battery())
        print("READY")

    def stream(self):
        self.tello.streamon()

    def land(self):
        self.tello.land()

    def takeoff(self):
        self.tello.send_command_without_return("takeoff")
        self.tello.is_flying = True

    def flip_left(self):
        if self.is_flying():
            self.stop()
            self.tello.flip_left()

    def flip_right(self):
        if self.is_flying():
            self.stop()
            self.tello.flip_right()

    def stop(self):
        self.x_velocity = 0
        self.y_velocity = 0
        self.z_velocity = 0
        self.yaw_velocity = 0
        self.fly()

    def fly(self):
        if self.is_flying():
            self.tello.send_rc_control(int(self.x_velocity), int(self.y_velocity), int(self.z_velocity), int(self.yaw_velocity))

    def disconnect(self):
        self.tello.end()

    def get_frame(self):
        return self.tello.get_frame_read().frame

    def get_height(self):
        return self.tello.get_height()

    def get_yaw(self):
        return self.tello.get_yaw()

    def is_flying(self):
        return self.get_height() > 0

    def fly_to(self, x, y, z, speed):
        self.tello.go_xyz_speed(int(x), int(y), int(z), int(speed))

    def rotate(self, yaw):
        if yaw < 0:
            self.tello.rotate_counter_clockwise(-int(yaw))
        else:
            self.tello.rotate_clockwise(int(yaw))
