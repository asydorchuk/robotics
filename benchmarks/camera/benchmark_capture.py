"""Comparison of OpenCV and PiCamera capture performance.

Main conclusions:
1) OpenCV is 6 times faster in camera captures: 30ms vs 180ms.
2) OpenCV has a lag of 8 frames, while PiCamera has no lag.
3) Considering lag PiCamera is preferable for computationally
intensive applications such as robotics, where it's extremely
important to get fresh sensor data in the feedback loop.
"""

from datetime import datetime as dt
import io
import time

import cv2
import picamera


def benchmark_opencv():
    camera = cv2.VideoCapture(0)
    timings = []
    # Do initial read to initialize camera.
    # The initial read is slightly slow.
    camera.read()
    for i in xrange(0, 10):
        start = dt.now()
        ret, frame = camera.read()
        stop = dt.now()
        ms = (stop - start).microseconds / 1000
        timings.append(ms)
    return timings


def benchmark_picamera():
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 60
    camera.vflip = True
    camera.start_preview()
    # Picamera requires minor delay before capture.
    time.sleep(1.0)
    timings = []
    for i in xrange(0, 10):
        stream = io.BytesIO()
        start = dt.now()
        camera.capture(stream, format='rgb', use_video_port=True)
        stop = dt.now()
        ms = (stop - start).microseconds / 1000
        timings.append(ms)
    camera.stop_preview()
    camera.close()
    return timings


def main():
    timings = benchmark_opencv()
    print 'OpenCV capture timings: %s' % timings

    timings = benchmark_picamera()
    print 'PiCamera capture timings: %s' % timings


if __name__ == '__main__':
    main()
