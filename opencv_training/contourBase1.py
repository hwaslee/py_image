# 참조: https://m.blog.naver.com/samsjang/220503082434
# cv2.bitwise_and() cv2.bitwise_not()

import numpy as np
import cv2
from datetime import datetime

def func_contour():
    tick = datetime.now()

    img = cv2.imread("../images/clearrect.png")
    # img = cv2.imread("../images/deskewed.png")
    # img = cv2.imread("../images/skewedSignature1.png")
    img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thr = cv2.threshold(img2gray, 127, 255, cv2.THRESH_BINARY_INV)
    # findContours() 테스트
    image, contours, hierarchy = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)         # RETR_LIST, RETR_TREE

    print('1,', type(image), len(image))
    print('2,', type(contours), len(contours), contours)

    for contour in contours:
        print('3, ', type(contour), contour)

    print('4, ', type(hierarchy), len(hierarchy), hierarchy)

    # findArea() 테스트

    cv2.drawContours(img, contours, -1, (0,0,255), 1)
    cv2.imshow('Contour', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


    tock = datetime.now()
    duration = tock - tick
    print("time elapsed: {:.2f} secs".format(duration.total_seconds()))


func_contour()