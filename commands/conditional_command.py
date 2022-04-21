from commands.command import Command


class ConditionalCommand(Command):

    def __init__(self, on_true: Command, on_false: Command, predicate):
        super().__init__(on_true.requirement)
        self.on_true = on_true
        self.on_false = on_false
        self.predicate = predicate
        self.command = on_true

    def initialize(self):
        if self.predicate():
            self.command = self.on_true
        else:
            self.command = self.on_false
        if self.command is not None:
            self.command.initialize()

    def execute(self):
        if self.command is not None:
            self.command.execute()

    def end(self, interrupted):
        if self.command is not None:
            self.command.end(interrupted)

    def is_finished(self):
        if self.command is None:
            return True
        return self.command.is_finished()
