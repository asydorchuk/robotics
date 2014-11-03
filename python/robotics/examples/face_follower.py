from datetime import datetime as dt
import io
import time

import cv2
import numpy as np
import picamera

from robotics.robots.factory import RobotFactory


def main():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    robot = RobotFactory.createAizekRobot()
    robot.start()
    camera = picamera.PiCamera()
    cwidth = 128
    cheight = 96
    camera.resolution = (cwidth, cheight)
    camera.framerate = 60
    camera.vflip = True
    camera.start_preview()
    time.sleep(1.0)

    while (True):
        stream = io.BytesIO()
        # Video port enables faster capture.
        # Rgb format allows to avoid expensive jpeg decoding.
        camera.capture(stream, format='rgb', use_video_port=True)
        frame = np.fromstring(stream.getvalue(), dtype=np.uint8).reshape((cheight, cwidth, 3))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        # Display image for debugging.
        cv2.imshow('frame', gray)
        cv2.waitKey(10)
        
        # Detect faces.
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        if len(faces) == 1:
            x, y, w, h = faces[0]
            cx = x + (w >> 1)
            cy = y + (h >> 1)
            print faces[0]
            print [cx, cy]
            cv2.rectangle(gray, (x,y), (x+w,y+h), (255,0,0), 2)
            if cy > cheight * 0.7 or min(w, h) < 25:
                robot.setControl(0.6, 0.6)
                time.sleep(0.2)
            elif cy < cheight * 0.3 or min(w, h) > 32:
                robot.setControl(-0.6, -0.6)
                time.sleep(0.2)
            elif cx < cwidth * 0.4:
                robot.setControl(0.6, -0.6)
                time.sleep(0.2)
            elif cx > cwidth * 0.6:
                robot.setControl(-0.6, 0.6)
                time.sleep(0.2)
            robot.setControl(0.0, 0.0)

    camera.stop_preview()
    carera.close()
    robot.stop()


if __name__ == '__main__':
    main()
