import time

from commands.command import Command
from filter.pid import PID
from utils import clamp


class PIDCommand(Command):

    def __init__(self, requirement, input_fn, output_fn, target, pid=PID(0, 0, 0), relative=False, timeout_fn=None):
        super().__init__(requirement)
        self.relative = relative
        self.pid = pid
        self.target = target
        self.output_fn = output_fn
        self.input_fn = input_fn
        self.initial_value = 0
        self.timeout_fn = timeout_fn
        self.start_time = None
        self.time_estimate = None
        self.last_time = None

    def initialize(self):
        self.start_time = time.time()
        self.last_time = time.time()
        if self.timeout_fn is None:
            self.time_estimate = None
        else:
            self.time_estimate = self.timeout_fn(self.pid.error_fn(self.__get_value(), self.target))
        if self.relative:
            self.initial_value = self.input_fn()
        else:
            self.initial_value = 0

    def execute(self):
        value = clamp(self.pid.calculate(self.__get_value(), self.target, time.time() - self.last_time), -1, 1)
        self.last_time = time.time()
        self.output_fn(value)

    def end(self, interrupted):
        self.output_fn(0)

    def is_finished(self):
        total_time = time.time() - self.start_time
        expired = False
        if self.time_estimate is not None:
            expired = total_time >= self.time_estimate
        return self.pid.at_setpoint() or expired

    def __get_value(self):
        return self.input_fn() - self.initial_value
