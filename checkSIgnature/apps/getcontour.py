# 직사각형 좌표를 찾는 방법.
# 원본은 contourBase2.py 참조
# 다만, approxPolyDP()의 epsilon 값을 이해한 후 변형하면서 테스트 필요 (19/01/05)
# param 설명 참조: https://opencv-python.readthedocs.io/en/latest/doc/15.imageContours/imageContours.html

import numpy as np
import cv2
import sys
import logging

'''
# import mylogging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s:%(level)s:%(filename)s:%(lineno)s: %(message)s")
file_handler = logging.FileHandler("mylogger.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
'''


def getRectCoordinate(fullImage):
    pos_X = 200
    pos_Y = 1700
    width = 1000
    height = 400
    image = fullImage[pos_Y:pos_Y+height, pos_X:pos_X+width]
    cv2.imshow("Signature", image)
    cv2.waitKey(0)

    # Hwa: image with 2 channels passed, so don't need to call cvtColor to make it gray
    # image = cv2.imread(fileName)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Hwa: With threshold of 240, successful to get coord of rectangle using contour in case of poor quality of image
    ret, threshed = cv2.threshold(image,
                                  240, 255, cv2.THRESH_BINARY_INV)

    ex, ey, ew, eh = None, None, None, None
    '''
    extContours, extHierarchy = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # logging.info('External Contours:', type(extContours), len(extContours))
    for contour in extContours:
        logging.info('contour:', type(contour), len(contour), contour)
        # posUL = contour[0]
        # posLL = contour[1]
        # posLR = contour[2]
        # posUR = contour[3]
        # print('UL:', posUL, 'UR:', posUR)
        # print('LL:', posLL, 'LR:', posLR)
        # xOfUL = posUL
        # logging.info('type(posUL): ', type(posUL))
        ex, ey, ew, eh = cv2.boundingRect(contour)
        if ew < 10 or eh < 10:
            continue
        else:
            break

    logging.info("External contour found.. x:{}, y:{}, w:{}, h:{}\n".format(ex, ey, ew, eh))
    '''

    # contours, hierarchy = cv2.findContours(threshed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count = 0;
    contourList = []
    logging.debug('How many contours: {}'.format(len(contours)))
    for contObj in contours:

        approx = cv2.approxPolyDP(contObj, 0.01*cv2.arcLength(contObj, True), True)
        count += 1

        if len(approx) == 4:
            contourSize = cv2.contourArea(contObj)
            ix, iy, iw, ih = cv2.boundingRect(contObj)
            logging.info("Each Rect contour found.. size:{}, x:{}, y:{}, w:{}, h:{}".format(contourSize, ix, iy, iw, ih))
            if ix == 0 or iy == 0 or contourSize < 20000 or contourSize > 30000:
                continue

            ### ix, iy, iw, ih = cv2.boundingRect(contour)
            ### logging.info("Rect Contour matched.. size:{}, x:{}, y:{}, w:{}, h:{}".format(contourSize, ix, iy, iw, ih))

            # exclude outer rectangle itself or smaller than threshold (width of the border line)
            # if ey == iy or abs(int(ew - iw)) > 10 or abs(int((ey + eh) - (iy + ih))) > 10:


            # logging.info ("square, ", count, type(contour), contour)
            # if count == 24:
            #    cv2.drawContours(img, [contour], -1, (0,0,255), 1)
            # else:
            #    cv2.drawContours(img, [contour], -1, (0,255,0), 1)
            ## cv2.drawContours(image, [contour], -1, (0,0,255), 1)
            # cv2.imshow('Contour selected'+str(count), image)

            contourList.append(contObj)

    # cv2.waitKey(0)

    # print('done.....')

    # cv2.imshow('Contour', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    del threshed
    del image
    return pos_X, pos_Y, contourList


if __name__ == '__main__':
    if len(sys.argv) == 1:
        contour = getRectCoordinate("../images/hkli_image.png", None)
        x, y, w, h = cv2.boundingRect(contour)
        logging.info("Signature contour found.. x:{}, y:{}, w:{}, h:{}".format(x, y, w, h))
        cv2.destroyAllWindows()
    else:
        getRectCoordinate(sys.argv[1])
