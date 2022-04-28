class Drone:
    def __init__(self):
        pass

    def takeoff(self):
        pass

    def land(self):
        pass

    def is_flying(self) -> bool:
        return False

    def stop(self):
        self.fly(0, 0, 0, 0, False)

    def emergency_stop(self):
        pass

    def fly(self, x: float, y: float, z: float, yaw: float, turbo: bool):
        pass

    def get_battery(self) -> float:
        return 0.0

    def get_altitude(self) -> float:
        return 0.0

    def get_yaw(self) -> float:
        return 0.0

    def get_frame(self):
        return None

    def set_headless(self, is_on: bool):
        pass

    def is_headless(self) -> bool:
        return False

    def is_holding_altitude(self) -> bool:
        return False

    def hold_altitude(self, is_on: bool):
        pass

    def flip(self, direction: int):
        pass
