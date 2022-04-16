from commands.command import Command


class ParallelRaceCommand(Command):

    def __init__(self, *commands: [Command]):
        requirements = list(filter(lambda c: c is not None, map(lambda c: c.requirement, commands)))
        requirement_set = set(requirements)
        if len(requirements) != len(requirement_set):
            raise Exception("Multiple commands can't require the same subsystem in a parallel command")
        # TODO: Make requirements a list
        super().__init__(requirements[0] if len(requirements) > 0 else None)
        self.commands = commands
        self.done = False

    def initialize(self):
        self.done = False
        for command in self.commands:
            command.initialize()

    def is_finished(self):
        return self.done

    def end(self, interrupted):
        for command in self.commands:
            command.end(interrupted)

    def execute(self):
        finished_command = None
        for command in self.commands:
            command.execute()
            if command.is_finished():
                command.end(False)
                finished_command = command
                self.done = True
                break

        if finished_command is not None:
            for command in self.commands:
                if command != finished_command:
                    command.end(True)


