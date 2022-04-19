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

        start = 16
        spacing = 32

        battery = easy_draw.Text(
            center_xy=(100, start)
        )
        height = easy_draw.Text(
            center_xy=(100, start + spacing)
        )
        time = easy_draw.Text(
            center_xy=(100, start + spacing * 2)
        )

        def update_values(event):
            battery.set_property(text='Battery: {} %'.format(self.drone.get_battery()))
            height.set_property(
                text='Height: {} ft'.format(round_places(self.drone.get_height_from_ground() * 0.0328084, 2)))
            time.set_property(text='Time: {} s'.format(self.drone.flight_time.read()))

        easy_draw.CANVAS.bind("<<update>>", update_values)

        easy_draw.end()

    def initialize(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def execute(self):
        easy_draw.CANVAS.event_generate("<<update>>")

    def is_finished(self):
        return False
