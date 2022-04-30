import threading

import cv2

from commands.PIDCommand import PIDCommand
from drone.drone import Drone
from filter.pid import PID
from utils import delta_angle


class AlignFaceCommand(PIDCommand):

    def __init__(self, drone: Drone):
        pid = PID(0.05, 0, 0.0005)
        pid.position_tolerance = 0
        pid.error_fn = self.calculate_error
        super().__init__(drone, self.get_position, self.set_velocity, 0.0, pid=pid)
        self.drone = drone
        self.classifier = cv2.CascadeClassifier('drone_commands/haarcascade_frontalface_default.xml')
        self.__running = False

    def initialize(self):
        super().initialize()
        self.__running = True
        threading.Thread(target=self.__detect, daemon=True).start()

    def __detect(self):
        while self.__running:
            img = self.drone.get_image()
            img = cv2.resize(img, (320, 240))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.classifier.detectMultiScale(gray, 1.1, 9)
            largest_size = 0
            largest_face = None
            for (x, y, w, h) in faces:
                size = w * h
                if size > largest_size:
                    largest_face = (x, y, w, h)
                    largest_size = size
            if largest_face is None:
                continue
            pct = (largest_face[0] / 320.0 - 0.5) * 2
            angle = pct * 45  # TODO: Determine actual FOV
            # size = largest_size / (320 * 240.0)
            # TODO: Allow vertical alignment
            self.target = self.drone.compass.read() + angle

    def set_velocity(self, velocity):
        self.drone.fly(0, 0, 0, velocity)

    def get_position(self):
        return self.drone.compass.read()

    def calculate_error(self, target, current):
        return delta_angle(current, target)

    def end(self, interrupted):
        super().end(interrupted)
        self.__running = False
