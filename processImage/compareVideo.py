import numpy as np
import cv2
from datetime import datetime


def showVideo():
    try:
        cap = cv2.VideoCapture(0)
    except:
        return

    cap.set(3, 480)
    cap.set(4, 320)

    numOfFrme = 0
    while True:
        ret, frame = cap.read()             # type(frame) : <class 'numpy.ndarray'>
        if not ret:
            print("Video failure")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Video', gray)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    tick = datetime.now()

    showVideo()

    tock = datetime.now()
    duration = tock - tick
    print("time elapsed: {:.2f} secs".format(duration.total_seconds()))
