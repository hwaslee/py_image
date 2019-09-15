# 참조: https://m.blog.naver.com/samsjang/220503082434
# cv2.bitwise_and() cv2.bitwise_not()

import numpy as np
import cv2
from datetime import datetime

def bitOperation(hpos, vpos):
    tick = datetime.now()

    img1 = cv2.imread("../images/watch.jpg")
    img2 = cv2.imread("../images/opencv_logo2.png")

    # 영역 지정
    rows, cols, channels = img2.shape
    roi = img1[vpos:vpos+rows, hpos:hpos+cols]

    # logo를 위한 mask, 역 mask 생성
    img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    cv2.imshow('img2gray', img2gray)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    print('--------------- mask ---------------')
    print(mask)
    cv2.imshow('mask', mask)
    mask_inv = cv2.bitwise_not(mask)
    print('--------------- mask inv ---------------')
    print(mask_inv)
    cv2.imshow('mask inv', mask_inv)

    # ROI에서 logo 부분만 검정색으로 만들기
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    cv2.imshow('img1_bg', img1_bg)

    # logo 이미지에서 logo 부분만 추출
    img2_fg = cv2.bitwise_and(img2, img2, mask=mask)
    cv2.imshow('img2_fg', img2_fg)

    # logo 이미지 배경을 cv2.add로 투명으로 만들고, ROI에 logo 이미지 넣기
    dest = cv2.add(img1_bg, img2_fg)
    img1[vpos:vpos+rows, hpos:hpos+cols] = dest

    cv2.imshow('result', img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    tock = datetime.now()
    duration = tock - tick
    print("time elapsed: {:.2f} secs".format(duration.total_seconds()))

bitOperation(10,10)