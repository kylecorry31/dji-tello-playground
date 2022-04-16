from commands.command import Command


class PerpetualCommand(Command):

    def __init__(self, command: Command):
        super().__init__(None)
        self.command = command

    def initialize(self):
        self.command.initialize()

    def execute(self):
        self.command.execute()

    def end(self, interrupted):
        self.command.end(interrupted)

    def is_finished(self):
        return False
