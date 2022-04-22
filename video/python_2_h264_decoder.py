import subprocess

import cv2
import numpy as np


class Python2H264Decoder:
    def __init__(self):
        self.process = subprocess.Popen("C:\\Users\\Kylec\\anaconda3\\envs\\tello2.7\\python.exe video/video.py",
                                        stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    def __del(self):
        self.process.kill()

    def decode(self) -> bytes:
        try:
            f = self.process.stdout.read(2073601)[:-1]
            if len(f) == 0:
                return None
            f = np.fromstring(f, dtype=np.ubyte, count=len(f), sep='')
            f = (f.reshape((720, int(2880 / 3), 3)))
            f = f[:, :960, :]
            f = cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
            return f
        except Exception as e:
            print(e)
            return None
