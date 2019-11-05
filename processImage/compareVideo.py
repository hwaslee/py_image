# import numpy as np
import cv2
from datetime import datetime


def showVideo():
    try:
        # cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture('/Volumes/NO NAME/20191021 영상기술검수 에러반려 예시/video black/N2018010300026_기술검수반려 [M]제왕수산 갈치  뷰티_갈치조림 (수정).MXF')

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
        print("파일 현재 위치(초), CAP_PROP_POS_MSEC(sec):", cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)

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
