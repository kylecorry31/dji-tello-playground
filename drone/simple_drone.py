from drone.advanced.tello_sdk import TelloSDK


class SimpleDrone:
    def __init__(self):
        self.tello = TelloSDK(print_responses=True)
        self.tello.command()
        self.tello.set_stream(True)
        print("READY")

    def land(self):
        self.tello.land()

    def takeoff(self):
        self.tello.takeoff()

    def is_flying(self):
        return self.tello.get_state().h != 0

    def stop(self):
        self.fly(0, 0, 0, 0)

    def fly(self, x, y, z, yaw, field_oriented=False, fast_mode=False):
        self.tello.rc(x, y, z, yaw)

    def go(self, x, listener=None):
        self.tello.move_y(x, listener)

    def emergency_stop(self):
        self.tello.emergency()
