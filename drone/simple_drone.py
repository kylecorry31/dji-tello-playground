from drone.advanced.tello2 import Tello2


class SimpleDrone:
    def __init__(self):
        self.tello = Tello2()
        self.tello.command()
        self.did_takeoff = False
        print("READY")

    def land(self):
        self.tello.land()
        self.did_takeoff = False

    def takeoff(self):
        self.tello.takeoff()
        self.did_takeoff = True

    def is_flying(self):
        return self.did_takeoff

    def stop(self):
        self.fly(0, 0, 0, 0)

    def fly(self, x, y, z, yaw, field_oriented=False, fast_mode=False):
        self.tello.rc(x, y, z, yaw)
