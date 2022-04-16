from commands.command import Command


class RepeatCommand(Command):

    def __init__(self, command: Command):
        super().__init__(command.requirement)
        self.command = command

    def initialize(self):
        self.command.initialize()

    def execute(self):
        self.command.execute()
        if self.command.is_finished():
            self.command.end(False)
            self.command.initialize()

    def end(self, interrupted):
        self.command.end(interrupted)

    def is_finished(self):
        return False
