from drone.advanced import sdk
from drone.advanced.udp_connection import UdpConnection
from drone.advanced.tello_state import parse_state, empty_state
from utils import clamp


class TelloSDK:
    def __init__(self, print_responses=False):
        self.state = empty_state()
        self.command_conn = UdpConnection('192.168.10.1', 8889, 8889)
        self.state_conn = UdpConnection('192.168.10.1', 8889, 8890)
        self.video_conn = UdpConnection('192.168.10.1', 8889, 11111, response_buffer_size=2048)
        if print_responses:
            self.command_conn.listen(self.__test_listener)
        # TODO: Expose a way to listen for frames
        self.state_conn.listen(self.__state_listener)

    def command(self):
        ret = self.command_conn.send(sdk.command(), wait=True)
        if ret is None or ret is sdk.error():
            raise Exception("Could not connect to Tello")

    def takeoff(self, listener=None):
        self.command_conn.send(sdk.takeoff(), response_listener=self.__create_ok_callback(listener))

    def land(self, listener=None):
        self.command_conn.send(sdk.land(), response_listener=self.__create_ok_callback(listener))

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

    def move_x(self, x: int, listener=None):
        if x > 0:
            self.command_conn.send(sdk.left(x), response_listener=self.__create_ok_callback(listener))
        else:
            self.command_conn.send(sdk.right(-x), response_listener=self.__create_ok_callback(listener))

    def move_y(self, y: int, listener=None):
        if y > 0:
            self.command_conn.send(sdk.forward(y), response_listener=self.__create_ok_callback(listener))
        else:
            self.command_conn.send(sdk.back(-y), response_listener=self.__create_ok_callback(listener))

    def move_z(self, z: int, listener=None):
        if z > 0:
            self.command_conn.send(sdk.up(z), response_listener=self.__create_ok_callback(listener))
        else:
            self.command_conn.send(sdk.down(-z), response_listener=self.__create_ok_callback(listener))

    def rotate(self, yaw: int, listener=None):
        if yaw > 0:
            self.command_conn.send(sdk.cw(yaw), response_listener=self.__create_ok_callback(listener))
        else:
            self.command_conn.send(sdk.ccw(-yaw), response_listener=self.__create_ok_callback(listener))

    def go(self, x: int, y: int, z: int, speed: float, listener=None):
        s = self.__percent(speed)
        self.command_conn.send(sdk.go(x, y, z, s), response_listener=self.__create_ok_callback(listener))

    def curve(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, speed: float, listener=None):
        s = self.__percent(speed)
        self.command_conn.send(sdk.curve(x1, y1, z1, x2, y2, z2, s),
                               response_listener=self.__create_ok_callback(listener))

    def __create_ok_callback(self, listener):
        def __callback(value: bytes, _):
            if listener is not None:
                listener(value == sdk.ok())
            return False

        return __callback

    def __read_value(self, cmd: bytes) -> float:
        return float(self.command_conn.send(cmd, wait=True).decode('utf-8'))

    def __read_vector(self, cmd: bytes) -> (float, float, float):
        value = self.command_conn.send(cmd, wait=True)
        if value is None:
            return None
        values = value.decode('utf-8').split(" ")
        if len(values) != 3:
            return None
        return float(values[0]), float(values[1]), float(values[2])

    def read_speed(self) -> float:
        return self.__read_value(sdk.read_speed())

    def read_battery(self) -> float:
        return self.__read_value(sdk.read_battery())

    def read_time(self) -> float:
        return self.__read_value(sdk.read_time())

    def read_height(self) -> float:
        return self.__read_value(sdk.read_height())

    def read_temp(self) -> float:
        return self.__read_value(sdk.read_temp())

    def read_attitude(self) -> (float, float, float):
        return self.__read_vector(sdk.read_attitude())

    def read_baro(self) -> float:
        return self.__read_value(sdk.read_baro())

    def read_acceleration(self) -> (float, float, float):
        return self.__read_vector(sdk.read_acceleration())

    def read_tof(self) -> float:
        return self.__read_value(sdk.read_tof())

    def read_wifi(self) -> float:
        return self.__read_value(sdk.read_wifi())

    def get_state(self):
        return self.state

    def __state_listener(self, value: bytes, _):
        self.state = parse_state(value)
        return True

    def __test_listener(self, value: bytes, _):
        print(value)
        return True

    def __percent(self, value: float) -> int:
        return int(clamp(value * 100, -100, 100))
