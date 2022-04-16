from commands.command import Command


class SequentialCommand(Command):

    def __init__(self, *commands: [Command]):
        # TODO: Make requirements a list
        super().__init__(commands[0].requirement)
        self.commands = commands
        self.idx = 0

    def initialize(self):
        self.idx = -1
        self.__next_command()

    def is_finished(self):
        return self.idx >= len(self.commands)

    def end(self, interrupted):
        if self.idx < len(self.commands):
            self.commands[self.idx].end(interrupted)

    def execute(self):
        if self.idx < len(self.commands):
            command = self.commands[self.idx]
            command.execute()
            if command.is_finished():
                command.end(False)
                self.__next_command()

    def __next_command(self):
        self.idx += 1
        if self.idx < len(self.commands):
            self.commands[self.idx].initialize()
