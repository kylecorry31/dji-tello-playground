import socket
import time
from threading import Thread
import libh264decoder
from sys import stdout

decoder = libh264decoder.H264Decoder()
socket_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_video.bind(('0.0.0.0', 11111))
frame = None


def _receive_video_thread():
    global frame
    packet_data = ""
    while True:
        try:
            res_string, ip = socket_video.recvfrom(2048)
            packet_data += res_string
            # end of frame
            if len(res_string) != 1460:
                for f in _h264_decode(packet_data):
                    frame = f
                if frame is not None:
                    stdout.write(frame)
                    stdout.flush()
                packet_data = ""
        except:
            pass


def _h264_decode(packet_data):
    res_frame_list = []
    frames = decoder.decode(packet_data)
    for framedata in frames:
        (f, w, h, ls) = framedata
        if f is not None:
            res_frame_list.append(f)

    return res_frame_list


receive_video_thread = Thread(target=_receive_video_thread)
receive_video_thread.daemon = True

time.sleep(1)
receive_video_thread.start()

while True:
    time.sleep(0.1)
