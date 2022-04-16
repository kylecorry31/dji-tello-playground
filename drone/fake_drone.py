import numpy as np


class FakeDrone:
    def __init__(self):
        self.x_speed = 50
        self.y_speed = 50
        self.z_speed = 50
        self.yaw_speed = 50
        self.x_velocity = 0
        self.y_velocity = 0
        self.z_velocity = 0
        self.yaw_velocity = 0
        self.is_flying = False
        print("READY")

    def land(self):
        self.is_flying = False
        print("LAND")

    def takeoff(self):
        self.is_flying = True
        print("TAKEOFF")

    def flip_left(self):
        if self.is_flying:
            self.stop()
            print("FLIP LEFT")

    def flip_right(self):
        if self.is_flying:
            self.stop()
            print("FLIP RIGHT")

    def stop(self):
        self.x_velocity = 0
        self.y_velocity = 0
        self.z_velocity = 0
        self.yaw_velocity = 0
        self.fly()

    def fly(self):
        if self.is_flying:
            print("Fly", self.x_velocity, self.y_velocity, self.z_velocity, self.yaw_velocity)

    def disconnect(self):
        print("DISCONNECT")

    def get_frame(self):
        return np.zeros((320, 240, 3), np.uint8)
