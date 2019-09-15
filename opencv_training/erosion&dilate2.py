# 참조 https://m.blog.naver.com/samsjang/220505815055
# Image Erosion (이미지 침식) and Dilation (팽창)

import numpy as np
import cv2

def morph():
    img = cv2.imread("../images/skewedSignature1.png", cv2.IMREAD_GRAYSCALE)

    max_value = np.max(img)
    backgroundRemoved = img.astype(float)
    blur = cv2.GaussianBlur(backgroundRemoved, (151,151), 50)
    backgroundRemoved = backgroundRemoved / blur
    backgroundRemoved = (backgroundRemoved * max_value / np.max(backgroundRemoved)).astype(np.uint8)
    ret, thres = cv2.threshold(backgroundRemoved, 130, 255, cv2.THRESH_BINARY)

    # remove horizontal lines
    kernel = np.ones((4, 1), np.uint8)
    dilation1 = cv2.dilate(thres, kernel, iterations=1)

    # remove vertical lines
    kernel = np.ones((1, 4), np.uint8)
    dilation2 = cv2.dilate(dilation1, kernel, iterations=1)

    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(dilation2, kernel, iterations=1)

    cv2.imshow("original", img)
    cv2.imshow("erosion", erosion)
    cv2.imshow("dilation 1", dilation1)
    cv2.imshow("dilation 2", dilation2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


morph()
