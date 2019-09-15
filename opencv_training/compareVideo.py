import numpy as np
import cv2
import time

def showVideo():
    try:
        cap = cv2.VideoCapture(0)
    except:
        return

    cap.set(3, 480)
    cap.set(4, 320)

    while True:
        ret, frame = cap.read()
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
    # execute only if run as a script
    now = time.gmtime(time.time())                  # 현재 시각 측정 후 해석
    now.tm_year, now.tm_mon, now.tm_mday            # 년, 월, 일
    (2017, 11, 14)
    showVideo()

