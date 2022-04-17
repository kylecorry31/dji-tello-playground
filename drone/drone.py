import logging
import struct
import socket

import djitellopy
from djitellopy import Tello
# from djitellopy.tello import client_socket

from drone.advanced import protocol
from drone.advanced.protocol import Packet
from drone.advanced.utils import byte
from utils import delta_angle, rotate


class Drone:
    def __init__(self):
        self.tello = djitellopy.Tello()
        self.tello.LOGGER.setLevel(logging.ERROR)
        self.tello.connect()
        self.yaw = None
        self.last_yaw = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 9001))
        print(self.tello.get_battery())
        print("READY")

    def stream(self):
        self.tello.streamon()

    def land(self):
        self.tello.land()

    def takeoff(self):
        self.__set_max_altitude_limit()
        self.tello.send_command_without_return("takeoff")
        self.tello.is_flying = True

    def flip_left(self):
        self.tello.flip_left()

    def flip_right(self):
        self.tello.flip_right()

    def stop(self):
        self.fly(0, 0, 0, 0)

    def fly(self, x, y, z, yaw, field_oriented=False, fast_mode=False):
        if field_oriented:
            rotated = rotate((x, y), self.get_yaw())
            x = rotated[0]
            y = rotated[1]
        if not fast_mode:
            self.tello.send_rc_control(int(x * 100), int(y * 100), int(z * 100), int(yaw * 100))
        else:
            pkt = Packet(protocol.STICK_CMD, 0x60)
            axis1 = int(1024 + 660.0 * x) & 0x7ff
            axis2 = int(1024 + 660.0 * y) & 0x7ff
            axis3 = int(1024 + 660.0 * z) & 0x7ff
            axis4 = int(1024 + 660.0 * yaw) & 0x7ff
            axis5 = int(fast_mode) & 0x01
            packed = axis1 | (axis2 << 11) | (
                    axis3 << 22) | (axis4 << 33) | (axis5 << 44)
            packed_bytes = struct.pack('<Q', packed)
            pkt.add_byte(byte(packed_bytes[0]))
            pkt.add_byte(byte(packed_bytes[1]))
            pkt.add_byte(byte(packed_bytes[2]))
            pkt.add_byte(byte(packed_bytes[3]))
            pkt.add_byte(byte(packed_bytes[4]))
            pkt.add_byte(byte(packed_bytes[5]))
            pkt.add_time()
            pkt.fixup()
            self.__send_packet(pkt)

    def disconnect(self):
        self.tello.end()

    def get_video(self):
        return self.tello.get_video_capture()

    def get_frame(self):
        return self.tello.get_frame_read().frame

    def get_height(self):
        return self.tello.get_height()

    def get_yaw(self):
        if self.yaw is None:
            self.reset_heading()
        current_yaw = self.tello.get_yaw()
        if current_yaw < 0:
            current_yaw += 360
        delta = delta_angle(self.last_yaw, current_yaw)
        self.last_yaw = current_yaw
        self.yaw += delta
        return self.yaw

    def is_flying(self):
        flying = self.get_height() > 0
        self.tello.is_flying = flying
        return flying

    def fly_to(self, x, y, z, speed):
        self.tello.go_xyz_speed(int(x), int(y), int(z), int(speed * 100))

    def rotate(self, yaw):
        if yaw < 0:
            self.tello.rotate_counter_clockwise(-int(yaw))
        else:
            self.tello.rotate_clockwise(int(yaw))

    def reset_heading(self):
        self.last_yaw = self.tello.get_yaw()
        self.yaw = 0

    def __set_max_altitude_limit(self):
        pkt = Packet(protocol.SET_ALT_LIMIT_CMD)
        pkt.add_byte(0x1e)  # 30m
        pkt.add_byte(0x00)
        pkt.fixup()
        self.__send_packet(pkt)

    def __send_packet(self, pkt):
        try:
            cmd = pkt.get_buffer()
            socket.sendto(cmd, self.tello.address)
        except Exception as err:
            return False

        return True
