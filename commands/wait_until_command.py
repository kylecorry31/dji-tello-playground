from commands.command import Command


class WaitUntilCommand(Command):
    def __init__(self, predicate):
        super().__init__(None)
        self.predicate = predicate

    def is_finished(self):
        return self.predicate()
