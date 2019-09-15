# 직사각형 좌표를 찾는 방법.
# 원본은 contourBase2.py 참조
# 다만, approxPolyDP()의 epsilon 값을 이해한 후 변형하면서 테스트 필요 (19/01/05)
# param 설명 참조: https://opencv-python.readthedocs.io/en/latest/doc/15.imageContours/imageContours.html

import numpy as np
import cv2
import sys



def getRectCoordinate(fileName):
    img = cv2.imread(fileName)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # With threshold value of 240, successful to get the coordinate of rectangle using contour
    ret, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    ex, ey, ew, eh = None, None, None, None
    # imgExtFound,      # error on windows with 3 return values
    extContours, extHierarchy = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print('External Contours:', type(extContours), len(extContours))
    for contour in extContours:
        # print('contour:', type(contour), len(contour), contour)
        # posUL = contour[0]
        # posLL = contour[1]
        # posLR = contour[2]
        # posUR = con tour[3]
        # print('UL:', posUL, 'UR:', posUR)
        # print('LL:', posLL, 'LR:', posLR)
        # xOfUL = posUL
        # print('type(posUL): ', type(posUL))
        ex, ey, ew, eh = cv2.boundingRect(contour)
        # print(ex, ey, ew, eh)

    # print('------------------------')

    # imgFound, \
    contours, hierarchy = cv2.findContours(threshed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    count = 0;
    # print('Len :', len(contours))
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
        count += 1

        if len(approx) == 4:
            ix, iy, iw, ih = cv2.boundingRect(contour)
            # exclude outer rectangle itself or smaller than threshold (width of the border line)
            if ex == ix or abs(int(ew - iw)) > 10 or abs(int((ey+eh) -(iy+ih))) > 10:
                continue

            # print ("square, ", count, type(contour), contour)
            # if count == 24:
            #    cv2.drawContours(img, [contour], -1, (0,0,255), 1)
            # else:
            #    cv2.drawContours(img, [contour], -1, (0,255,0), 1)
            cv2.drawContours(img, [contour], -1, (0,0,255), 1)

            print(ix, iy, iw, ih)
            pass
        elif len(approx) == 5:
            # print ("pentagon, ", count)
            # cv2.drawContours(img, [contour], -1, (0,0,255), 1)
            pass
        elif len(approx) == 3:
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

    print('done.....')

    cv2.imshow('Contour',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # getRectCoordinate("../images/Signature.png")
        # getRectCoordinate("../images/skewedSignature1.png")
        getRectCoordinate("../images/deskewed.png")
    else:
        getRectCoordinate(sys.argv[1])