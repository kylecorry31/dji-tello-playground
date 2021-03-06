from drone.advanced import sdk, proc
from drone.advanced.udp_connection import UdpConnection
from drone.advanced.tello_state import parse_state, empty_state
from utils import clamp


class TelloSDK:
    def __init__(self, print_responses=False):
        self.__state = empty_state()
        self.__has_valid_state = False
        self.__command_conn = UdpConnection('192.168.10.1', 8889, 8889)
        self.__state_conn = UdpConnection('192.168.10.1', 8889, 8890)
        if print_responses:
            self.__command_conn.listen(self.__test_listener)
        self.__state_conn.listen(self.__state_listener)
        self.__video_conn = UdpConnection('192.168.10.1', 8889, 11111, response_buffer_size=2048, auto_connect=False)

    def command(self):
        ret = self.__command_conn.send(sdk.command(), wait=True)
        if ret is None or ret is sdk.error():
            raise Exception("Could not connect to Tello")

    def set_altitude_limit(self, limit: int):
        self.__command_conn.send(proc.altitude_limit(limit))

    def takeoff(self, manual=False, listener=None):
        if manual:
            self.stick(-1, -1, -1, 1, False)
        else:
            self.__command_conn.send(sdk.takeoff(), response_listener=self.__create_ok_callback(listener))

    def throw_and_go(self):
        self.__command_conn.send(proc.throw_and_go())

    def land(self, listener=None):
        self.__command_conn.send(sdk.land(), response_listener=self.__create_ok_callback(listener))

    def palm_land(self):
        self.__command_conn.send(proc.palm_land())

    def rc(self, x: float, y: float, z: float, yaw: float):
        self.__command_conn.send(sdk.rc(self.__percent(x), self.__percent(y), self.__percent(z),
                                        self.__percent(yaw)))

    def video(self, listener):
        self.__video_conn.connect()
        self.__video_conn.listen(listener)

    def set_stream(self, is_on: bool):
        if is_on:
            self.__command_conn.send(sdk.streamon())
        else:
            self.__command_conn.send(sdk.streamoff())

    def emergency(self):
        self.__command_conn.send(sdk.emergency())

    def move_x(self, x: int, listener=None):
        if x > 0:
            self.__command_conn.send(sdk.forward(x), response_listener=self.__create_ok_callback(listener))
        else:
            self.__command_conn.send(sdk.back(-x), response_listener=self.__create_ok_callback(listener))

    def move_y(self, y: int, listener=None):
        if y > 0:
            self.__command_conn.send(sdk.left(y), response_listener=self.__create_ok_callback(listener))
        else:
            self.__command_conn.send(sdk.right(-y), response_listener=self.__create_ok_callback(listener))

    def move_z(self, z: int, listener=None):
        if z > 0:
            self.__command_conn.send(sdk.up(z), response_listener=self.__create_ok_callback(listener))
        else:
            self.__command_conn.send(sdk.down(-z), response_listener=self.__create_ok_callback(listener))

    def rotate(self, yaw: int, listener=None):
        if yaw > 0:
            self.__command_conn.send(sdk.cw(yaw), response_listener=self.__create_ok_callback(listener))
        else:
            self.__command_conn.send(sdk.ccw(-yaw), response_listener=self.__create_ok_callback(listener))

    def go(self, x: int, y: int, z: int, speed: float, listener=None):
        s = self.__percent(speed)
        self.__command_conn.send(sdk.go(y, x, z, s), response_listener=self.__create_ok_callback(listener))

    def curve(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, speed: float, listener=None):
        s = self.__percent(speed)
        self.__command_conn.send(sdk.curve(x1, y1, z1, x2, y2, z2, s),
                                 response_listener=self.__create_ok_callback(listener))

    def flip(self, direction: int):
        self.__command_conn.send(proc.flip(direction))

    def set_video_mode(self, wide: bool):
        self.__command_conn.send(proc.set_video_mode(wide))

    def disconnect(self):
        self.__command_conn.cancel()
        self.__state_conn.cancel()
        if self.__video_conn is not None:
            self.__video_conn.cancel()

    def read_speed(self, callback=None) -> float:
        return self.__read_value(sdk.read_speed(), callback)

    def read_battery(self, callback=None) -> float:
        return self.__read_value(sdk.read_battery(), callback)

    def read_time(self, callback=None) -> float:
        return self.__read_value(sdk.read_time(), callback)

    def read_height(self, callback=None) -> float:
        return self.__read_value(sdk.read_height(), callback)

    def read_temp(self, callback=None) -> float:
        return self.__read_value(sdk.read_temp(), callback)

    def read_attitude(self) -> (float, float, float):
        return self.__read_vector(sdk.read_attitude())

    def read_baro(self, callback=None) -> float:
        return self.__read_value(sdk.read_baro(), callback)

    def read_acceleration(self) -> (float, float, float):
        return self.__read_vector(sdk.read_acceleration())

    def read_tof(self, callback=None) -> float:
        return self.__read_value(sdk.read_tof(), callback)

    def read_wifi(self, callback=None) -> float:
        return self.__read_value(sdk.read_wifi(), callback)

    def has_valid_state(self):
        return self.__has_valid_state

    def get_state(self):
        return self.__state

    def stick(self, x: float, y: float, z: float, yaw: float, fast_mode: bool):
        self.__command_conn.send(
            proc.stick(self.__percent(x), self.__percent(y), self.__percent(z), self.__percent(yaw), fast_mode))

    def __create_ok_callback(self, listener):
        def __callback(value: bytes, _):
            if listener is not None:
                listener(value == sdk.ok())
            return False

        return __callback

    def __create_value_callback(self, listener):
        def __callback(value: bytes, _):
            if listener is not None:
                listener(float(value.decode('utf-8')))
            return False

        return __callback

    def __read_value(self, cmd: bytes, callback=None) -> float:
        if callback is None:
            return float(self.__command_conn.send(cmd, wait=True).decode('utf-8'))
        else:
            self.__command_conn.send(cmd, response_listener=self.__create_value_callback(callback))

    def __read_vector(self, cmd: bytes) -> (float, float, float):
        value = self.__command_conn.send(cmd, wait=True)
        if value is None:
            return None
        values = value.decode('utf-8').split(" ")
        if len(values) != 3:
            return None
        return float(values[0]), float(values[1]), float(values[2])

    def __state_listener(self, value: bytes, _):
        self.__state = parse_state(value)
        self.__has_valid_state = True
        return True

    def __test_listener(self, value: bytes, _):
        print(value)
        return True

    def __percent(self, value: float) -> int:
        return int(clamp(value * 100, -100, 100))
