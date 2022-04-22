import threading

import cv2

from commands.command import Command
from video.tello_camera import TelloCamera


class ShowVideoCommand(Command):

    def __init__(self):
        super().__init__(None)
        # TODO: Inject the camera
        self.camera = TelloCamera()
        self.__running = False
        self.__display_thread = threading.Thread(target=self.__display, daemon=True)

    def initialize(self):
        self.__running = True
        self.camera.start()
        self.__display_thread.start()

    def end(self, interrupted):
        self.camera.stop()
        self.__running = False
        cv2.destroyWindow("Tello")

    def is_finished(self):
        return False

    def __display(self):
        while self.__running:
            frame = self.camera.frame
            if frame is not None:
                cv2.imshow("Tello", frame)
            cv2.waitKey(100)
