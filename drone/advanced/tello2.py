from drone.advanced import sdk
from drone.advanced.udp_connection import UdpConnection
from drone.advanced.tello_state import parse_state, empty_state
from utils import clamp


class Tello2:
    def __init__(self):
        self.state = empty_state()
        self.command_conn = UdpConnection('192.168.10.1', 8889, 8889)
        self.state_conn = UdpConnection('192.168.10.1', 8889, 8890)
        self.video_conn = UdpConnection('192.168.10.1', 8889, 11111, response_buffer_size=2048)
        # TODO: Expose a way to listen for frames
        self.state_conn.listen(self.__state_listener)

    def command(self):
        ret = self.command_conn.send(sdk.command(), wait=True)
        if ret is None or ret is sdk.error():
            raise Exception("Could not connect to Tello")

    def takeoff(self):
        self.command_conn.send(sdk.takeoff())

    def land(self):
        self.command_conn.send(sdk.land())

    def rc(self, x: float, y: float, z: float, yaw: float):
        self.command_conn.send(sdk.rc(self.__percent(x), self.__percent(y), self.__percent(z),
                                      self.__percent(yaw)))

    def set_stream(self, is_on: bool):
        if is_on:
            self.command_conn.send(sdk.streamon())
        else:
            self.command_conn.send(sdk.streamoff())

    def emergency(self):
        self.command_conn.send(sdk.emergency())

    def move_x(self, x: int):
        if x > 0:
            self.command_conn.send(sdk.left(x))
        else:
            self.command_conn.send(sdk.right(-x))

    def move_y(self, y: int):
        if y > 0:
            self.command_conn.send(sdk.forward(y))
        else:
            self.command_conn.send(sdk.back(-y))

    def move_z(self, z: int):
        if z > 0:
            self.command_conn.send(sdk.up(z))
        else:
            self.command_conn.send(sdk.down(-z))

    def rotate(self, yaw: int):
        if yaw > 0:
            self.command_conn.send(sdk.cw(yaw))
        else:
            self.command_conn.send(sdk.ccw(-yaw))

    def go(self, x: int, y: int, z: int, speed: float):
        s = self.__percent(speed)
        self.command_conn.send(sdk.go(x, y, z, s))

    def curve(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, speed: float):
        s = self.__percent(speed)
        self.command_conn.send(sdk.curve(x1, y1, z1, x2, y2, z2, s))

    def flip(self, direction: chr):
        self.command_conn.send(sdk.flip(direction))

    def get_state(self):
        return self.state

    def __state_listener(self, value: bytes):
        self.state = parse_state(value)

    def __percent(self, value: float) -> int:
        return int(clamp(value * 100, -100, 100))
