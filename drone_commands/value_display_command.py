import threading
from commands import Command
from drone.drone import Drone
from ui import easy_draw


def round_places(num, places):
    return round(num * 10 ** places) / 10 ** places


class ValueDisplayCommand(Command):
    def __init__(self, drone: Drone):
        super().__init__(None)
        self.drone = drone
        self.thread = None

    def run(self):
        easy_draw.load_canvas('#ffffff')

        start = 12
        spacing = 24

        battery = easy_draw.Text(
            center_xy=(100, start),
            size=12
        )
        height = easy_draw.Text(
            center_xy=(100, start + spacing),
            size=12
        )
        yaw = easy_draw.Text(
            center_xy=(100, start + spacing * 2),
            size=12
        )

        def update_values(event):
            CM_TO_FT = 0.0328084
            battery.set_property(text='Battery: {} %'.format(self.drone.get_battery()))
            height.set_property(
                text='Height: {} ft'.format(round_places(self.drone.get_altitude() * CM_TO_FT, 2)))
            yaw.set_property(text='Yaw: {}'.format(self.drone.get_yaw()))

        easy_draw.CANVAS.bind("<<update>>", update_values)

        easy_draw.end()

    def initialize(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def execute(self):
        easy_draw.CANVAS.event_generate("<<update>>")

    def is_finished(self):
        return False
