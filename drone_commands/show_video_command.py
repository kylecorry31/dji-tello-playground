import threading

import cv2

from commands.command import Command
from drone.drone import Drone


class ShowVideoCommand(Command):

    def __init__(self, drone: Drone):
        super().__init__(None)
        self.drone = drone
        self.__running = False
        self.__display_thread = threading.Thread(target=self.__display, daemon=True)

    def initialize(self):
        self.__running = True
        self.__display_thread.start()

    def end(self, interrupted):
        self.__running = False
        cv2.destroyWindow("Tello")

    def is_finished(self):
        return not self.__running

    def __display(self):
        while self.__running:
            frame = self.drone.get_image()
            if frame is not None:
                cv2.imshow("Tello", frame)
            cv2.waitKey(1)
