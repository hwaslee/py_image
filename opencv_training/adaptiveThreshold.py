# 참조 https://m.blog.naver.com/samsjang/220504782549
import numpy as np
import cv2


def applyAdaptiveThreshold():

    ### added 1
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions


    print ('--------- color 이미지 속성 -----------')
    # img = cv2.imread("../images/skewedSignature1.png", cv2.IMREAD_GRAYSCALE)
    img = cv2.imread("/Volumes/USB3-64/Image/HKFMI/deskewedImage.png", cv2.IMREAD_GRAYSCALE)
    img_h, img_w = img.shape


    thresh_value = 127
    blocksize = 21
    compensation = 2
    ret, thr1 = cv2.threshold(img, thresh_value, 255, cv2.THRESH_BINARY)
    thr2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blocksize, compensation)
    thr3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, compensation)

    titles = ['original', 'Global Thresholding(v=127)', 'Adaptive MEAN', 'Adaptive GAUSSIAN']
    images = [ img, thr1, thr2, thr3]

    for i in range(4):
        # images[i] = cv2.resize(images[1], (600, 900))

        ### added 2
        imS = cv2.resize(images[i], (int(img_w/2.5), int(img_h/2.5)))  # Resize image
        cv2.imshow(titles[i], imS)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


applyAdaptiveThreshold()