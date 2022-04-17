import time

from commands.command import Command
from utils import clamp


class PIDCommand(Command):

    def __init__(self, requirement, input_fn, output_fn, target, p=0, i=0, d=0, threshold=0, relative=False,
                 error_fn=None,
                 timeout_fn=None):
        super().__init__(requirement)
        self.relative = relative
        self.threshold = threshold
        self.d = d
        self.i = i
        self.p = p
        self.target = target
        self.output_fn = output_fn
        self.input_fn = input_fn
        self.initial_value = 0
        if error_fn is not None:
            self.error_fn = error_fn
        else:
            self.error_fn = self.__default_error_fn
        self.timeout_fn = timeout_fn
        self.start_time = None
        self.time_estimate = None

    def initialize(self):
        self.start_time = time.time()
        if self.timeout_fn is None:
            self.time_estimate = None
        else:
            self.time_estimate = self.timeout_fn(self.__get_error())
        if self.relative:
            self.initial_value = self.input_fn()
        else:
            self.initial_value = 0

    def execute(self):
        error = self.__get_error()
        value = clamp(error * self.p, -1, 1)
        self.output_fn(value)

    def end(self, interrupted):
        self.output_fn(0)

    def is_finished(self):
        total_time = time.time() - self.start_time
        expired = False
        if self.time_estimate is not None:
            expired = total_time >= self.time_estimate
        error = abs(self.__get_error())
        return error <= self.threshold or expired

    def __get_error(self):
        return self.error_fn(self.target, self.__get_value())

    def __get_value(self):
        return self.input_fn() - self.initial_value

    def __default_error_fn(self, target, current):
        return target - current
