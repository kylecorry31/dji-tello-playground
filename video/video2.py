import io
import socket
from threading import Thread
import numpy as np
import cv2

from video.python_2_h264_decoder import Python2H264Decoder

decoder = Python2H264Decoder()
# socket_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# socket_video.bind(('0.0.0.0', 11111))
frame = None


def _receive_video_thread():
    global frame
    # packet_data = io.BytesIO()
    while True:
        try:
            # res_string, ip = socket_video.recvfrom(2048)
            # packet_data.write(res_string)
            # end of frame
            # if len(res_string) != 1460:
                # for f in _h264_decode(packet_data.getvalue()):
                #     frame = cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
            f = decoder.decode()#packet_data.getvalue())
            if f is not None:
                # print(f)
                frame = f
                # packet_data.close()
                # packet_data = io.BytesIO()

        except socket.error as exc:
            print("Caught exception socket.error : %s" % exc)


# def _h264_decode(packet_data):
#     res_frame_list = []
#     framedata = decoder.decode(packet_data, 2000, 2000)
#     if framedata is not None:
#         ls = 2880
#         w = 720
#         h = 480
#         f = framedata
#         # (f, w, h, ls) = framedata
#         if f is not None:
#             f = np.frombuffer(f, dtype=np.ubyte)
#             f = (f.reshape((h, ls / 3, 3)))
#             f = f[:, :w, :]
#             res_frame_list.append(f)
#
#     return res_frame_list


receive_video_thread = Thread(target=_receive_video_thread)
receive_video_thread.daemon = True
receive_video_thread.start()

while True:
    try:
        f = frame
        if f is not None:
            cv2.imshow("Tello", f)
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
    except Exception as e:
        pass
