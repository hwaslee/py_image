# https://m.blog.naver.com/samsjang/220507996391

import numpy as np
import cv2
import matplotlib.pyplot as plt



def canny():
    # img = cv2.imread('../images/clearrect.png', cv2.IMREAD_GRAYSCALE)
    img = cv2.imread('../images/skewedSignature1.png', cv2.IMREAD_GRAYSCALE)

    edge1 = cv2.Canny(img, 50, 200)
    edge2 = cv2.Canny(img, 100, 200)
    edge3 = cv2.Canny(img, 170, 200)
    edge4 = cv2.Canny(img, 40, 40)

    cv2.imshow('original', img)
    cv2.imshow('Canny  Edge1', edge1)
    cv2.imshow('Canny  Edge2', edge2)
    cv2.imshow('Canny  Edge3', edge3)
    cv2.imshow('Canny  Edge4', edge4)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


canny()