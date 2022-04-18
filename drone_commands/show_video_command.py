import subprocess
import threading

import cv2

from commands.command import Command
from drone.drone import Drone


class ShowVideoCommand(Command):

    def __init__(self, drone: Drone):
        super().__init__(None)
        self.drone = drone
        self.process = None

    def initialize(self):
        self.drone.stream()
        # TODO: Create a virtual environment for this
        self.process = subprocess.Popen("C:\\Users\\Kylec\\anaconda3\\envs\\tello2.7\\python.exe video/video.py",
                                        stderr=subprocess.DEVNULL)

    def end(self, interrupted):
        if interrupted and self.process is not None:
            self.process.kill()

    def is_finished(self):
        return False
