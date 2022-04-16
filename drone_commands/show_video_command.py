import cv2

from commands.command import Command
from drone.drone import Drone


class ShowVideoCommand(Command):

    def __init__(self, drone: Drone):
        super().__init__(None)
        self.drone = drone

    def execute(self):
        cv2.imshow("Tello", self.drone.get_frame())

    def is_finished(self):
        return False
