import time

from drone.advanced.tello_protocol import TelloProtocol

tello = TelloProtocol(print_responses=True)
tello.connect()

try:
    tello.takeoff()
    time.sleep(4)
    tello.land()
    time.sleep(1)
except KeyboardInterrupt:
    print("STOP")

tello.emergency()
