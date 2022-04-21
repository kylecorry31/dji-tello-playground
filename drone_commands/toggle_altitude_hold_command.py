from commands import Command


class ToggleAltitudeHoldCommand(Command):
    def __init__(self, drone):
        super().__init__(None)
        self.drone = drone

    def initialize(self):
        if self.drone.altitude_hold_module.is_enabled:
            self.drone.altitude_hold_module.is_enabled = False
        else:
            self.drone.altitude_hold_module.is_enabled = True
            self.drone.altitude_hold_module.reset()

    def is_finished(self):
        return True
