class CommandRunner:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if CommandRunner.__instance is None:
            CommandRunner()
        return CommandRunner.__instance

    def __init__(self):
        if CommandRunner.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CommandRunner.__instance = self
        self.active_commands = []
        self.default_commands = []

    def update(self):
        commands_to_remove = []
        commands_to_start = []
        for command in self.active_commands:
            command.execute()
            if command.is_finished():
                command.end(False)
                commands_to_remove.append(command)
                for default_cmd in self.default_commands:
                    if default_cmd.requirement == command.requirement:
                        commands_to_start.append(default_cmd)
        for command in commands_to_remove:
            self.active_commands.remove(command)

        for command in commands_to_start:
            self.schedule(command, False)

    def schedule(self, command, interrupt=True):
        commands_to_remove = []
        for c in self.active_commands:
            if c.requirement == command.requirement and c.requirement is not None:
                if not interrupt:
                    return
                c.end(True)
                commands_to_remove.append(c)
        for c in commands_to_remove:
            self.active_commands.remove(c)

        self.active_commands.append(command)
        command.initialize()

    def cancel(self, command):
        if command in self.active_commands:
            command.end(True)
            self.active_commands.remove(command)
            for cmd in self.default_commands:
                self.schedule(cmd, False)

    def remove_default_command(self, command):
        if command in self.active_commands:
            command.end(True)

        self.active_commands.remove(command)
        self.default_commands.remove(command)

    def set_default_command(self, command):
        if command.requirement is None:
            return
        commands_to_remove = []
        for c in self.default_commands:
            if c.requirement == command.requirement:
                commands_to_remove.append(c)
        for c in commands_to_remove:
            self.default_commands.remove(c)

        self.default_commands.append(command)
        self.schedule(command, False)

    def cancel_all(self, prevent_default=False):
        for c in self.active_commands:
            c.end(True)
        self.active_commands = []

        if not prevent_default:
            for cmd in self.default_commands:
                self.schedule(cmd, False)
