import djitellopy


class Drone:
    def __init__(self):
        self.x_velocity = 0
        self.y_velocity = 0
        self.z_velocity = 0
        self.yaw_velocity = 0
        self.tello = djitellopy.Tello()
        self.tello.connect()
        self.tello.streamon()
        print("READY")

    def land(self):
        self.tello.land()

    def takeoff(self):
        self.tello.takeoff()

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
        self.tello.send_control_command("stop")

    def fly(self):
        if self.is_flying():
            self.tello.send_rc_control(self.x_velocity, self.y_velocity, self.z_velocity, self.yaw_velocity)

    def disconnect(self):
        self.tello.end()

    def get_frame(self):
        return self.tello.get_frame_read().frame

    def get_height(self):
        return self.tello.get_height()

    def get_yaw(self):
        return self.tello.get_yaw()

    def is_flying(self):
        return self.tello.is_flying

    def fly_to(self, x, y, z, speed):
        self.tello.go_xyz_speed(x, y, z, speed)

    def rotate(self, yaw):
        if yaw < 0:
            self.tello.rotate_counter_clockwise(-yaw)
        else:
            self.tello.rotate_clockwise(yaw)
