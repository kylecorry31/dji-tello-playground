from drone.advanced import sdk, proc
from drone.advanced.udp_connection import UdpConnection
from drone.advanced.tello_state import parse_state, empty_state
from utils import clamp


class TelloProtocol:
    def __init__(self, print_responses=False):
        self.command_conn = UdpConnection('192.168.10.1', 8889, 9000)
        # self.log_conn = UdpConnection('192.168.10.1', 8889, 11111, response_buffer_size=2048)
        if print_responses:
            self.command_conn.listen(self.__print_responses)

    def __print_responses(self, value, addr):
        print(value, addr)
        return True

    def connect(self):
        self.command_conn.send("command".encode("utf-8"), wait=True)#"command".encode("utf-8"))

    def takeoff(self):
        self.command_conn.send(proc.takeoff())

    def land(self):
        self.command_conn.send(proc.land())

    def emergency(self):
        self.command_conn.send(proc.emergency())
