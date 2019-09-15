# 참조 https://m.blog.naver.com/samsjang/220504782549
import numpy as np
import cv2


def applyThreshold():
    print ('--------- color 이미지 속성 -----------')
    img = cv2.imread("../images/skewedSignature1.png", cv2.IMREAD_GRAYSCALE)

    thresh_value = 100
    ret, thr1 = cv2.threshold(img, thresh_value, 255, cv2.THRESH_BINARY)
    ret, thr2 = cv2.threshold(img, thresh_value, 255, cv2.THRESH_BINARY_INV)
    ret, thr3 = cv2.threshold(img, thresh_value, 255, cv2.THRESH_TRUNC)
    ret, thr4 = cv2.threshold(img, thresh_value, 255, c)
    ret, thr5 = cv2.threshold(img, thresh_value, 255, cv2.THRESH_TOZERO_INV)

    cv2.imshow('original', img)
    cv2.imshow('BINARY', thr1)
    cv2.imshow('BINARY_INV', thr2)
    cv2.imshow('TRUNC', thr3)
    cv2.imshow('TOZERO', thr4)
    cv2.imshow('TOZERO_INV', thr5)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


applyThreshold()