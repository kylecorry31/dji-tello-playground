import socket
import time
from threading import Thread
import libh264decoder
import numpy as np
import cv2

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
                    frame = f#cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
                if frame is not None:
                    # print len(frame)
                    print frame,
                    pass
                packet_data = ""

        except socket.error as exc:
            print("Caught exception socket.error : %s" % exc)


def _h264_decode(packet_data):
    res_frame_list = []
    frames = decoder.decode(packet_data)
    for framedata in frames:
        (f, w, h, ls) = framedata
        if f is not None:
            # print(h)
            # f = np.fromstring(f, dtype=np.ubyte, count=len(f), sep='')
            # f = (f.reshape((h, ls / 3, 3)))
            # f = f[:, :w, :]
            res_frame_list.append(f)

    return res_frame_list


receive_video_thread = Thread(target=_receive_video_thread)
receive_video_thread.daemon = True
receive_video_thread.start()

while True:
    time.sleep(0.1)

# while True:
#     try:
#         f = frame
#         if f is not None:
#             cv2.imshow("Tello", f)
#         if cv2.waitKey(1) & 0xFF == ord('x'):
#             break
#     except Exception as e:
#         pass
