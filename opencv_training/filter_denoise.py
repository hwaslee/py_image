# https://m.blog.naver.com/samsjang/220505080672

import numpy as np
import cv2


def onMouse(x):
    pass

def blurring():
    img = cv2.imread('../images/clearrect.png')

    cv2.namedWindow('BlurPane')
    cv2.createTrackbar('Blur_Mode', 'BlurPane', 0, 2, onMouse)
    cv2.createTrackbar('Blur', 'BlurPane', 0, 5, onMouse)

    mode = cv2.getTrackbarPos('Blur_Mode', 'BlurPane')
    val = cv2.getTrackbarPos('Blur', 'BlurPane')

    while True:
        val = val*2 + 1

        try:
            if mode == 0:
                blur = cv2.blur(img, (val, val))
            elif mode ==  1:
                blur = cv2.GaussianBlur(img, (val, val), 0)
            elif mode == 2:
                blur = cv2.medianBlur(img, val)
            else:
                break

            cv2.imshow('BlurPane', blur)
        except:
            break

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

        mode = cv2.getTrackbarPos('Blur_Mode', 'BlurPane')
        val = cv2.getTrackbarPos('Blur', 'BlurPane')

    cv2.destroyAllWindows()


blurring()