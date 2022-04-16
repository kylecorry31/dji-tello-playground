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
        self.fly()

    def fly(self):
        if self.is_flying():
            self.tello.send_rc_control(self.x_velocity, self.y_velocity, self.z_velocity, self.yaw_velocity)

    def disconnect(self):
        self.tello.end()

    def get_frame(self):
        return self.tello.get_frame_read().frame

    def get_height(self):
        return self.tello.get_height()

    def is_flying(self):
        return self.tello.is_flying
