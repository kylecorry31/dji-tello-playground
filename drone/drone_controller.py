from XInput import *

from .drone import Drone


class DroneController(EventHandler):

    def __init__(self, drone: Drone, *controllers):
        super().__init__(*controllers)
        self.drone = drone
        self.gamepad_thread = GamepadThread(self, auto_start=False)

    def stop(self):
        self.gamepad_thread.stop()

    def start(self):
        self.gamepad_thread.start()

    def process_button_event(self, event):
        if event.button_id == BUTTON_LEFT_SHOULDER:
            if event.type == EVENT_BUTTON_PRESSED:
                self.drone.z_velocity = -self.drone.z_speed
            else:
                self.drone.z_velocity = 0

        if event.button_id == BUTTON_RIGHT_SHOULDER:
            if event.type == EVENT_BUTTON_PRESSED:
                self.drone.z_velocity = self.drone.z_speed
            else:
                self.drone.z_velocity = 0

        if event.button_id == BUTTON_A:
            if event.type == EVENT_BUTTON_PRESSED:
                if self.drone.is_flying:
                    self.drone.land()
                else:
                    self.drone.takeoff()

        if event.button_id == BUTTON_X:
            if event.type == EVENT_BUTTON_PRESSED:
                self.drone.flip_left()

        if event.button_id == BUTTON_B:
            if event.type == EVENT_BUTTON_PRESSED:
                self.drone.flip_right()

        if event.button_id == BUTTON_START:
            if event.type == EVENT_BUTTON_PRESSED:
                self.drone.stop()

    def process_trigger_event(self, event):
        pass

    def process_stick_event(self, event):
        if event.stick == 1:
            self.drone.x_velocity = event.x * self.drone.x_speed
            self.drone.y_velocity = event.y * self.drone.y_speed

        if event.stick == 0:
            self.drone.yaw_velocity = event.x * self.drone.yaw_speed

    def process_connection_event(self, event):
        pass
