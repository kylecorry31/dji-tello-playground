import cv2

from commands.command import Command
from drone.drone import Drone


class ShowVideoCommand(Command):

    def __init__(self, drone: Drone):
        super().__init__(None)
        self.drone = drone
        self.drone.stream()

    def execute(self):
        try:
            img = self.drone.get_frame()
            img = cv2.resize(img, (480, 320))
            cv2.imshow("Tello", img)
        except Exception as e:
            pass

    def is_finished(self):
        return False
