import cv2

from video.tello_camera import TelloCamera

camera = TelloCamera()
camera.start()

while True:
    try:
        f = camera.frame
        if f is not None:
            cv2.imshow("Tello", f)
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
    except Exception as e:
        pass
