# 이것이 직사각형 좌표를 찾는 방법일 듯.
# 다만, approxPolyDP()의 epsilon 값을 이해한 후 변형하면서 테스트 필요 (19/01/05)
# param 설명 참조: https://opencv-python.readthedocs.io/en/latest/doc/15.imageContours/imageContours.html

import numpy as np
import cv2


# img = cv2.imread("../images/clearrect.png")
# img = cv2.imread("../images/deskewed.png")
# img = cv2.imread("../images/skewedSignature1.png")
img = cv2.imread("../images/Signature.png")
# img = cv2.imread("../images/skewedSignature1.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

ex, ey, ew, eh = None, None, None, None
imgExtFound, extContours, extHierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print('External Contours:', type(extContours), len(extContours))
for contour in extContours:
    print('contour:', type(contour), len(contour), contour)
    posUL = contour[0]
    posLL = contour[1]
    posLR = contour[2]
    posUR = contour[3]
    print('UL:', posUL, 'UR:', posUR)
    print('LL:', posLL, 'LR:', posLR)
    xOfUL = posUL
    print('type(posUL): ', type(posUL))
    ex, ey, ew, eh = cv2.boundingRect(contour)
    print(ex, ey, ew, eh)

print('------------------------')

imgFound, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
count = 0;
print('Len :', len(contours))
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True), True)
    count  += 1

    if len(approx)==4:
        ix, iy, iw, ih = cv2.boundingRect(contour)
        if abs(int(ew-iw))>10 or abs(int(eh-ih))<10 :
            continue

        print ("square, ", count, type(contour), contour)
        if count == 24:
            cv2.drawContours(img, [contour], -1, (0,0,255), 1)
        else:
            cv2.drawContours(img, [contour], -1, (0,255,0), 1)

        print(ix, iy, iw, ih)
        pass
    elif len(approx)==5:
        # print ("pentagon, ", count)
        # cv2.drawContours(img, [contour], -1, (0,0,255), 1)
        pass
    elif len(approx)==3:
        # print ("triangle, ", count)
        # cv2.drawContours(img, [contour], -1, (0,255,0), 1)
        pass
    elif len(approx) == 9:
        # print ("half-circle, ", count)
        # cv2.drawContours(img, [contour], -1, (255,255,0), 1)
        pass
    elif len(approx) > 15:
        # print ("circle, ", count)
        # cv2.drawContours(img, [contour], -1, (0,255,255), 1)
        pass

cv2.imshow('Contour',img)
cv2.waitKey(0)
cv2.destroyAllWindows()