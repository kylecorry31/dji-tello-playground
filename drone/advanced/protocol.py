import datetime
import struct
from io import BytesIO

from .crc import *
from .utils import *

# low-level Protocol (https://tellopilots.com/wiki/protocol/#MessageIDs)
START_OF_PACKET = 0xcc
SSID_MSG = 0x0011
SSID_CMD = 0x0012
SSID_PASSWORD_MSG = 0x0013
SSID_PASSWORD_CMD = 0x0014
WIFI_REGION_MSG = 0x0015
WIFI_REGION_CMD = 0x0016
WIFI_MSG = 0x001a
VIDEO_ENCODER_RATE_CMD = 0x0020
VIDEO_DYN_ADJ_RATE_CMD = 0x0021
EIS_CMD = 0x0024
VIDEO_START_CMD = 0x0025
VIDEO_RATE_QUERY = 0x0028
TAKE_PICTURE_COMMAND = 0x0030
VIDEO_MODE_CMD = 0x0031
VIDEO_RECORD_CMD = 0x0032
EXPOSURE_CMD = 0x0034
LIGHT_MSG = 0x0035
JPEG_QUALITY_MSG = 0x0037
ERROR_1_MSG = 0x0043
ERROR_2_MSG = 0x0044
VERSION_MSG = 0x0045
TIME_CMD = 0x0046
ACTIVATION_TIME_MSG = 0x0047
LOADER_VERSION_MSG = 0x0049
STICK_CMD = 0x0050
TAKEOFF_CMD = 0x0054
LAND_CMD = 0x0055
FLIGHT_MSG = 0x0056
SET_ALT_LIMIT_CMD = 0x0058
FLIP_CMD = 0x005c
THROW_AND_GO_CMD = 0x005d
PALM_LAND_CMD = 0x005e
TELLO_CMD_FILE_SIZE = 0x0062  # pt50
TELLO_CMD_FILE_DATA = 0x0063  # pt50
TELLO_CMD_FILE_COMPLETE = 0x0064  # pt48
SMART_VIDEO_CMD = 0x0080
SMART_VIDEO_STATUS_MSG = 0x0081
LOG_HEADER_MSG = 0x1050
LOG_DATA_MSG = 0x1051
LOG_CONFIG_MSG = 0x1052
BOUNCE_CMD = 0x1053
CALIBRATE_CMD = 0x1054
LOW_BAT_THRESHOLD_CMD = 0x1055
ALT_LIMIT_MSG = 0x1056
LOW_BAT_THRESHOLD_MSG = 0x1057
ATT_LIMIT_CMD = 0x1058  # Stated incorrectly by Wiki (checked from raw packets)
ATT_LIMIT_MSG = 0x1059

EMERGENCY_CMD = 'emergency'

# Flip commands taken from Go version of code
# FlipFront flips forward.
FlipFront = 0
# FlipLeft flips left.
FlipLeft = 1
# FlipBack flips backwards.
FlipBack = 2
# FlipRight flips to the right.
FlipRight = 3
# FlipForwardLeft flips forwards and to the left.
FlipForwardLeft = 4
# FlipBackLeft flips backwards and to the left.
FlipBackLeft = 5
# FlipBackRight flips backwards and to the right.
FlipBackRight = 6
# FlipForwardRight flips forwards and to the right.
FlipForwardRight = 7


class Packet(object):
    def __init__(self, cmd, pkt_type=0x68, payload=b''):
        if isinstance(cmd, str):
            self.buf = bytearray()
            for c in cmd:
                self.buf.append(ord(c))
        elif isinstance(cmd, (bytearray, bytes)):
            self.buf = bytearray()
            self.buf[:] = cmd
        else:
            self.buf = bytearray([
                START_OF_PACKET,
                0, 0,
                0,
                pkt_type,
                (cmd & 0xff), ((cmd >> 8) & 0xff),
                0, 0])
            self.buf.extend(payload)

    def fixup(self, seq_num=0):
        buf = self.get_buffer()
        if buf[0] == START_OF_PACKET:
            buf[1], buf[2] = le16(len(buf) + 2)
            buf[1] = (buf[1] << 3)
            buf[3] = crc8(buf[0:3])
            buf[7], buf[8] = le16(seq_num)
            self.add_int16(crc16(buf))

    def get_buffer(self):
        return self.buf

    def get_data(self):
        return self.buf[9:len(self.buf) - 2]

    def add_byte(self, val):
        self.buf.append(val & 0xff)

    def add_int16(self, val):
        self.add_byte(val)
        self.add_byte(val >> 8)

    def add_time(self, time=datetime.datetime.now()):
        self.add_int16(time.hour)
        self.add_int16(time.minute)
        self.add_int16(time.second)
        self.add_int16(int(time.microsecond / 1000) & 0xff)
        self.add_int16((int(time.microsecond / 1000) >> 8) & 0xff)

    def get_time(self, buf=None):
        if buf is None:
            buf = self.get_data()[1:]
        hour = int16(buf[0], buf[1])
        min = int16(buf[2], buf[3])
        sec = int16(buf[4], buf[5])
        millisec = int16(buf[6], buf[8])
        now = datetime.datetime.now()
        return datetime.datetime(now.year, now.month, now.day, hour, min, sec, millisec)
