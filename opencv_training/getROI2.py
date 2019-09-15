# 참조: https://m.blog.naver.com/samsjang/220502203203

import numpy as np
import cv2


print ('--------- 이미지, 이미지 부분영역 속성 보기 -----------')
img = cv2.imread("../images/watch.jpg")
cv2.imshow("original", img)

subimg = img[195:300, 250:375]
cv2.imshow('cutting', subimg)

img[195:300, 250:375] = subimg

print(img.shape)
print(subimg.shape)

cv2.imshow('modified', img)

cv2.waitKey(0)
cv2.destroyAllWindows()


print ('--------- 이미지 색별로 분리 (not recommend to use) -----------')
b, g, r = cv2.split(img)
print(img[100,100])
print(b[100,100], g[100,100], r[100,100])

cv2.imshow('blue channel', b)
cv2.imshow('green channel', g)
cv2.imshow('red channel', r)

cv2.waitKey(0)
cv2.destroyAllWindows()

print ('--------- 이미지 색별로 분리 (better than previous one) -----------')
b = img[:, :, 0]
g = img[:, :, 1]
r = img[:, :, 2]

cv2.imshow('blue channel(2)', b)
cv2.imshow('green channel(2)', g)
cv2.imshow('red channel(2)', r)

cv2.waitKey(0)
cv2.destroyAllWindows()

