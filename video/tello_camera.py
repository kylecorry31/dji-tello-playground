import subprocess
import threading

import cv2
import numpy as np


class TelloCamera:
    def __init__(self):
        self.process = None
        self.__thread = threading.Thread(target=self.__get_frames, daemon=True)
        self.frame = None

    def start(self):
        self.process = subprocess.Popen("C:\\Users\\Kylec\\anaconda3\\envs\\tello2.7\\python.exe video/video.py",
                                        stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.__thread.start()

        # TODO: Send the process a start signal

    def stop(self):
        if self.process is not None:
            self.process.kill()
            self.process = None

    def __get_frames(self):
        height = 720
        width = 960
        while self.process is not None:
            try:
                f = self.process.stdout.read(width * height * 3 + 1)[:-1]
                if len(f) == 0:
                    continue
                f = np.fromstring(f, dtype=np.ubyte, count=len(f), sep='')
                f = (f.reshape((height, width, 3)))
                f = f[:, :width, :]
                self.frame = cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
            except Exception as e:
                print(e)
