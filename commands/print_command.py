from commands.command import Command


class PrintCommand(Command):
    def __init__(self, value):
        super().__init__(None)
        self.value = value

    def initialize(self):
        print(self.value)

    def is_finished(self):
        return True
