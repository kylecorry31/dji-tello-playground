from commands.command import Command


class ParallelCommand(Command):

    def __init__(self, *commands: [Command]):
        requirements = list(filter(lambda c: c is not None, map(lambda c: c.requirement, commands)))
        requirement_set = set(requirements)
        if len(requirements) != len(requirement_set):
            raise Exception("Multiple commands can't require the same subsystem in a parallel command")
        # TODO: Make requirements a list
        super().__init__(requirements[0] if len(requirements) > 0 else None)
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
                command.end(False)
                to_remove.append(command)
        for command in to_remove:
            self.remaining.remove(command)
