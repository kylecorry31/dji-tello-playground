from drone.advanced.tello import Tello
from drone.sensors.accelerometer import Accelerometer
from drone.sensors.sensor import Sensor


class LinearAccelerometer(Sensor):
    def __init__(self, accelerometer: Accelerometer):
        self.accelerometer = accelerometer

    def read(self):
        acc = self.accelerometer.read()
        return acc[0], acc[1], acc[2] + 1000

    def update(self):
        self.accelerometer.update()

    def reset(self):
        self.accelerometer.reset()
