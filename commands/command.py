class Command:

    def __init__(self, requirement):
        self.requirement = requirement

    def initialize(self):
        pass

    def execute(self):
        pass

    def is_finished(self):
        return False

    def end(self, interrupted):
        pass
