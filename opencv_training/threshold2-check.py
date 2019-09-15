# 참조 https://m.blog.naver.com/samsjang/220504782549
import numpy as np
import cv2


def applyThreshold():
    print ('--------- color 이미지 속성 -----------')
    img = cv2.imread("../images/skewedSignature1.png", cv2.IMREAD_GRAYSCALE)

    imgs = []
    for thresh_value in range(0, 255, 20):
        print(thresh_value)
        ret, thr = cv2.threshold(img, thresh_value, 255, cv2.THRESH_BINARY)
        imgs.append(thr)

    print("# of Images: {}".format(str(len(imgs))))

    cv2.imshow("Original", img)

    index = 0
    for newImg in imgs:
        cv2.imshow(str(index) + " image", newImg)
        index += 1

    cv2.waitKey(0)
    cv2.destroyAllWindows()


applyThreshold()