from commands.command_runner import CommandRunner
from commands.command import Command


class CancelCommand(Command):

    def __init__(self, command: Command):
        super().__init__(None)
        self.command = command

    def initialize(self):
        CommandRunner.get_instance().cancel(self.command)

    def is_finished(self):
        return True
