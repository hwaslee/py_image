# 참조: https://m.blog.naver.com/samsjang/220502203203

import numpy as np
import cv2

print ('--------- color 이미지 속성 -----------')
img = cv2.imread("../images/watch.jpg")

# 340,200 위치 픽셀 값
px = img[340, 200]

# pixel의 B,G,R 값 및 이미지 속성을 출력
print (px)
print(img.shape)
print(img.size)
print(img.dtype)

height, width, channels = img.shape
print("Heiht:{}, Width:{}, Channels:{}".format(height, width, channels))

print ('---------- gray 이미지 속성 ----------')
gray = cv2.imread("../images/watch.jpg", cv2.IMREAD_GRAYSCALE)

# 340,200 위치 픽셀 값
px = gray[340, 200]

# gray pixel값 및 이미지 속성을 출력
print (px)
print(gray.shape)
print(gray.size)
print(gray.dtype)

height, width = gray.shape[:2]
print("Heiht:{}, Width:{}, Channels:{}".format(height, width, None))

print ('--------- pixle의 color 분리 조사 -----------')
B = img.item(340, 200, 0)
G = img.item(340, 200, 1)
R = img.item(340, 200, 2)
bgr = [B, G, R]
print (bgr)

print ('--------- pixle의 color 변경 (to Black) -----------')
cv2.imshow('before', img)
cv2.waitKey(0)
img[0,0] = [0,0,0]
img[0,1] = [0,0,0]
img[0,2] = [0,0,0]
img[0,3] = [0,0,0]
img[0,4] = [0,0,0]
img[0,5] = [0,0,0]

cv2.imshow('after', img)
cv2.waitKey(0)

