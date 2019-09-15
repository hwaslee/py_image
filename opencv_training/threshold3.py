# 참조 https://m.blog.naver.com/samsjang/220504782549
import numpy as np
import cv2
import matplotlib.pyplot as plt

def threshold3():
    img = cv2.imread("..\\..\\..\\captcha-master\\test-set\\1.png", cv2.IMREAD_GRAYSCALE)
    # img = cv2.imread("../images/skewedSignature1.png", cv2.IMREAD_GRAYSCALE)

    # global threshold 적용
    thresh_value = 20
    ret, thr1 = cv2.threshold(img, thresh_value, 255, cv2.THRESH_BINARY)

    # Otsu Binary generation
    ret, thr2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # OTSU Binary generation after applying Gaussian Blur
    blur = cv2.GaussianBlur(img, (5,5), 0)
    ret, thr3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    titles = ['original noisy', 'Histogram', "G-Thresholding",
              'original noisy', 'Histogram', "Otsu Thresholding",
              'Gaussian Filtered', 'Histogram', "Otsu Thresholding"]

    images = [img, 0,  thr1, img, 0, thr2, blur, 0, thr3]

    for i in range(3):
        plt.subplot(3,3,i*3+1)
        plt.imshow(images[i*3], 'gray')
        plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])

        plt.subplot(3,3,i*3+2)
        plt.hist(images[i*3].ravel(), 256)
        plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])

        plt.subplot(3,3,i*3+3)
        plt.imshow(images[i*3+2], 'gray')
        plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])

    plt.show()

threshold3()