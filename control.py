import time
import cv2

from drone.drone import Drone
from drone.drone_controller import DroneController

drone = Drone()
controller = DroneController(drone, 0)
controller.start()
while True:
    drone.fly()
    cv2.imshow("Tello", drone.get_frame())
    time.sleep(0.02)
