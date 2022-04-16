from commands.command import Command


class ParallelCommand(Command):

    def __init__(self, commands: [Command]):
        # TODO: Make requirements a list
        super().__init__(commands[0].requirement)
        self.commands = commands
        self.remaining = []

    def initialize(self):
        self.remaining = [*self.commands]
        for command in self.remaining:
            command.initialize()

    def is_finished(self):
        return len(self.remaining) == 0

    def end(self, interrupted):
        for command in self.remaining:
            command.end(interrupted)

    def execute(self):
        to_remove = []
        for command in self.remaining:
            command.execute()
            if command.is_finished():
                command.end()
                to_remove.append(command)
        for command in to_remove:
            self.remaining.remove(command)
