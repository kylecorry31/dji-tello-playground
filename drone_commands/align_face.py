import cv2

from commands.PIDCommand import PIDCommand
from drone.drone import Drone
from filter.pid import PID


class AlignFaceCommand(PIDCommand):

    def __init__(self, drone: Drone):
        pid = PID(0.02, 0.2, 0)
        pid.integrator_limit = 0.8
        pid.integrator_range = 8
        pid.position_tolerance = 1
        pid.error_fn = self.calculate_error
        super().__init__(drone, self.get_face, self.set_velocity, 0.0, pid=pid, relative=False,
                         timeout_fn=self.estimate_time)
        self.drone = drone
        self.classifier = cv2.CascadeClassifier('drone_commands/haarcascade_frontalface_default.xml')

    def set_velocity(self, velocity):
        self.drone.fly(0, 0, 0, velocity)

    def estimate_time(self, error):
        return abs(error) * 5

    def get_face(self):
        # TODO: Do this in the background
        # TODO: Align vertically
        img = self.drone.get_image()
        img = cv2.resize(img, (320, 240))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.classifier.detectMultiScale(gray, 1.1, 5)
        largest_size = 0
        largest_face = None
        for (x, y, w, h) in faces:
            size = w * h
            if size > largest_size:
                largest_face = (x, y, w, h)
                largest_size = size
        if largest_face is None:
            return 0.0 # TODO: Seek if face not seen recently
        pct = (largest_face[0] / 320.0 - 0.5) * 2
        angle = -pct * 45
        size = largest_size / (320 * 240.0)
        return angle

    def calculate_error(self, target, current):
        return target - current
