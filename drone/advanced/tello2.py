from drone.advanced import api
from drone.advanced.connection import Connection
from utils import clamp


class Tello2:
    def __init__(self):
        self.connection = Connection('192.168.10.1', 8889, 8889)

    def command(self):
        ret = self.connection.send(api.command(), wait=True)
        if ret is None or ret is api.error():
            raise Exception("Could not connect to Tello")

    def takeoff(self):
        self.connection.send(api.takeoff())

    def land(self):
        self.connection.send(api.land())

    def rc(self, x: float, y: float, z: float, yaw: float):
        self.connection.send(api.rc(self.__percent(x), self.__percent(y), self.__percent(z),
                                    self.__percent(yaw)))

    def set_stream(self, is_on: bool):
        if is_on:
            self.connection.send(api.streamon())
        else:
            self.connection.send(api.streamoff())

    def emergency(self):
        self.connection.send(api.emergency())

    def move_x(self, x: int):
        if x > 0:
            self.connection.send(api.left(x))
        else:
            self.connection.send(api.right(-x))

    def move_y(self, y: int):
        if y > 0:
            self.connection.send(api.forward(y))
        else:
            self.connection.send(api.back(-y))

    def move_z(self, z: int):
        if z > 0:
            self.connection.send(api.up(z))
        else:
            self.connection.send(api.down(-z))

    def rotate(self, yaw: int):
        if yaw > 0:
            self.connection.send(api.cw(yaw))
        else:
            self.connection.send(api.ccw(-yaw))

    def go(self, x: int, y: int, z: int, speed: float):
        s = self.__percent(speed)
        self.connection.send(api.go(x, y, z, s))

    def curve(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, speed: float):
        s = self.__percent(speed)
        self.connection.send(api.curve(x1, y1, z1, x2, y2, z2, s))

    def __percent(self, value: float) -> int:
        return int(clamp(value * 100, -100, 100))