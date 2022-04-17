import threading

import cv2

from commands.command import Command
from drone.drone import Drone


class ShowVideoCommand(Command):

    def __init__(self, drone: Drone):
        super().__init__(None)
        self.drone = drone
        self.show_thread = threading.Thread(target=self.__show_video)
        self.read_thread = threading.Thread(target=self.__read_video)
        self.read_thread.daemon = True
        self.stopped = False
        self.frame = None

    def initialize(self):
        self.stopped = False
        self.drone.stream()
        self.show_thread.start()
        self.read_thread.start()

    def end(self, interrupted):
        self.stopped = True
        self.show_thread.join()
        self.read_thread.join()

    def __read_video(self):
        video = self.drone.get_video()
        video.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        video.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
        while not self.stopped:
            try:
                if video.isOpened():
                    ret, img = video.read()
                    if ret:
                        self.frame = img
            except Exception as e:
                pass

    def __show_video(self):
        while not self.stopped:
            try:
                f = self.frame
                if f is not None:
                    # f = cv2.resize(f, (480, 320))
                    cv2.imshow("Tello", f)
                # time.sleep(1 / 30)
                if cv2.waitKey(1) & 0xFF == ord('x'):
                    break
            except Exception as e:
                pass

    def is_finished(self):
        return self.stopped
