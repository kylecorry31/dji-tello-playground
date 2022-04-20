import struct

from drone.advanced.protocol import Packet
from drone.advanced.utils import le16, byte


def connection_request() -> bytes:
    port = 11111
    b = le16(port)
    buf = 'conn_req:%c%c' % (chr(b[0]), chr(b[1]))
    return buf.encode('utf-8')


def takeoff() -> bytes:
    pkt = Packet(0x0054)
    pkt.fixup()
    return pkt.buf


def land() -> bytes:
    pkt = Packet(0x0055)
    pkt.add_byte(0x00)
    pkt.fixup()
    return pkt.buf


def ack_log(id: int) -> bytes:
    pkt = Packet(0x1050, 0x50)
    pkt.add_byte(0x00)
    b0, b1 = le16(id)
    pkt.add_byte(b0)
    pkt.add_byte(b1)
    pkt.fixup()
    return pkt.buf


def emergency() -> bytes:
    return "emergency".encode("utf-8")


def stick(x: int, y: int, z: int, yaw: int, fast_mode: bool):
    cmd = 0x0050
    pkt = Packet(cmd, 0x60)
    axis1 = int(1024 + 660.0 * x / 100.0) & 0x7ff
    axis2 = int(1024 + 660.0 * y / 100.0) & 0x7ff
    axis3 = int(1024 + 660.0 * z / 100.0) & 0x7ff
    axis4 = int(1024 + 660.0 * yaw / 100.0) & 0x7ff
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
    return pkt.buf


def altitude_limit(limit: int) -> bytes:
    cmd = 0x0058
    pkt = Packet(cmd)
    pkt.add_byte(byte(limit))
    pkt.add_byte(0x00)
    pkt.fixup()
    return pkt.buf


def flip(direction: int) -> bytes:
    cmd = 0x005c
    pkt = Packet(cmd, 0x70)
    pkt.add_byte(direction)
    pkt.fixup()
    return pkt.buf


def set_video_mode(zoom: bool) -> bytes:
    cmd = 0x0031
    pkt = Packet(cmd)
    pkt.add_byte(int(zoom))
    pkt.fixup()
    return pkt.buf
