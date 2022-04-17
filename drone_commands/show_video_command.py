import threading

import cv2

from commands.command import Command
from drone.drone import Drone


class ShowVideoCommand(Command):

    def __init__(self, drone: Drone):
        super().__init__(None)
        self.drone = drone
        self.thread = threading.Thread(target=self.__show_video)
        self.stopped = False

    def initialize(self):
        self.stopped = False
        self.drone.stream()
        self.thread.start()

    def end(self, interrupted):
        self.stopped = True
        self.thread.join()

    def __show_video(self):
        while not self.stopped:
            try:
                img = self.drone.get_frame()
                img = cv2.resize(img, (480, 320))
                cv2.imshow("Tello", img)
                if cv2.waitKey(1) & 0xFF == ord('x'):
                    break
            except Exception as e:
                pass

    def is_finished(self):
        return self.stopped
