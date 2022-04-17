from XInput import *
from commands import *

A = BUTTON_A
B = BUTTON_B
X = BUTTON_X
Y = BUTTON_Y
START = BUTTON_START
BACK = BUTTON_BACK
LB = BUTTON_LEFT_SHOULDER
RB = BUTTON_RIGHT_SHOULDER
LEFT_THUMB = BUTTON_LEFT_THUMB
RIGHT_THUMB = BUTTON_RIGHT_THUMB
DPAD_UP = BUTTON_DPAD_UP
DPAD_DOWN = BUTTON_DPAD_DOWN
DPAD_LEFT = BUTTON_DPAD_LEFT
DPAD_RIGHT = BUTTON_DPAD_RIGHT
LEFT_STICK = 0
RIGHT_STICK = 1
LT = 0
RT = 1


class XboxController(EventHandler):

    def __init__(self, id):
        super().__init__(id)
        self.gamepad_thread = GamepadThread(self, auto_start=True)
        self.button_commands = []
        self.buttons = {}
        self.triggers = {}
        self.sticks = {}

    def __del__(self):
        self.gamepad_thread.stop()

    def get_button(self, button_id: int) -> bool:
        if button_id not in self.buttons:
            return False
        return self.buttons[button_id]

    def get_trigger(self, trigger_id: int) -> float:
        if trigger_id not in self.triggers:
            return 0.0
        return self.triggers[trigger_id]

    def get_y(self, stick_id: int) -> float:
        if stick_id not in self.sticks:
            return 0.0
        return self.sticks[stick_id][1]

    def get_x(self, stick_id: int) -> float:
        if stick_id not in self.sticks:
            return 0.0
        return self.sticks[stick_id][0]

    def while_held(self, button_id: int, command: Command):
        cmd = RepeatCommand(command)
        self.when_pressed(button_id, cmd)
        self.when_released(button_id, CancelCommand(cmd))

    def when_pressed(self, button_id: int, command: Command):
        to_remove = []
        for cmd in self.button_commands:
            if cmd[0] == button_id and cmd[1] == EVENT_BUTTON_PRESSED:
                to_remove.append(cmd)

        for cmd in to_remove:
            self.button_commands.remove(cmd)

        if command is not None:
            self.button_commands.append((button_id, EVENT_BUTTON_PRESSED, command))

    def when_released(self, button_id: int, command: Command):
        to_remove = []
        for cmd in self.button_commands:
            if cmd[0] == button_id and cmd[1] == EVENT_BUTTON_RELEASED:
                to_remove.append(cmd)

        for cmd in to_remove:
            self.button_commands.remove(cmd)

        if command is not None:
            self.button_commands.append((button_id, EVENT_BUTTON_RELEASED, command))

    def process_button_event(self, event):
        if event.type == EVENT_BUTTON_PRESSED:
            self.buttons[event.button_id] = True
        elif event.type == EVENT_BUTTON_RELEASED:
            self.buttons[event.button_id] = False

        for cmd in self.button_commands:
            if cmd[0] == event.button_id and cmd[1] == event.type:
                CommandRunner.get_instance().schedule(cmd[2], True)

    def process_trigger_event(self, event):
        self.triggers[event.trigger] = event.value

    def process_stick_event(self, event):
        self.sticks[event.stick] = (event.x, event.y)

    def process_connection_event(self, event):
        pass
