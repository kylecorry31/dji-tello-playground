from commands.command import Command
import time


class WaitCommand(Command):

    def __init__(self, seconds: float):
        super().__init__(None)
        self.seconds = seconds
        self.start_time = None

    def initialize(self):
        self.start_time = time.time()

    def is_finished(self):
        return time.time() - self.start_time >= self.seconds
