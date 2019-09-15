# 참조 https://m.blog.naver.com/samsjang/220505815055
# Image Erosion (이미지 침식) and Dilation (팽창)

import numpy as np
import cv2

def morph():
    img1 = cv2.imread("../images/skewedSignature1.png", cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread("../images/skewedSignature1.png", cv2.IMREAD_GRAYSCALE)
