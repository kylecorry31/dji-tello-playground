import subprocess
import threading

import cv2
import numpy as np


class TelloCamera:
    def __init__(self):
        self.process = None
        self.__thread = threading.Thread(target=self.__get_frames, daemon=True)
        self.__frame = None

    def start(self):
        self.process = subprocess.Popen(
            "C:\\Users\\Kylec\\anaconda3\\envs\\tello2.7\\python.exe video/python2_h264_udp_decoder.py",
            stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.__thread.start()

        # TODO: Send the process a start signal

    def stop(self):
        if self.process is not None:
            self.process.kill()
            self.process = None

    def __del__(self):
        self.stop()

    def get_frame(self):
        height = 720
        width = 960
        f = self.__frame
        if f is None:
            return None
        f = np.fromstring(f, dtype=np.ubyte, count=len(f), sep='')
        f = (f.reshape((height, width, 3)))
        f = f[:, :width, :]
        return cv2.cvtColor(f, cv2.COLOR_RGB2BGR)

    def __get_frames(self):
        height = 720
        width = 960
        while self.process is not None:
            try:
                f = self.process.stdout.read(width * height * 3)
                if len(f) == 0:
                    continue
                self.__frame = f
            except Exception as e:
                print(e)
