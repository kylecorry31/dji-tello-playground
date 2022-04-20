from commands import Command
from drone.simple_drone import SimpleDrone


class TestCommand(Command):
    def __init__(self, drone: SimpleDrone):
        super().__init__(drone)
        self.drone = drone
        self.is_done = False

    def initialize(self):
        self.is_done = False

        def __callback(_):
            self.is_done = True

        self.drone.go(50, __callback)

    def is_finished(self):
        return self.is_done
