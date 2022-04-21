from commands import Command


class ToggleHeadlessCommand(Command):
    def __init__(self, drone):
        super().__init__(None)
        self.drone = drone

    def initialize(self):
        if self.drone.headless_module.is_enabled:
            self.drone.headless_module.is_enabled = False
        else:
            self.drone.headless_module.is_enabled = True
            self.drone.headless_module.reset()

    def is_finished(self):
        return True
