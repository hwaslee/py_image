# main program to check if signature exists or not for SLI
#
import numpy as np
import cv2
import os
import sys
import argparse
import correct_skew
import getcontour
import pyperclip
import logging

'''
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
formatter = logging.Formatter("%(asctime)s:%(level)s:%(filename)s:%(lineno)s: %(message)s")
file_handler = logging.FileHandler("mylogger.log")
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
'''

margin = 3
SignWhiteRate = 99.9

def genResult(results):
    index = 0
    texts = ''
    for result in results:
        if index == 0:
            texts += ('계약자 성명: ' + result[2] + "\n")
        elif index == 1:
            texts += ('계약자 서명: ' + result[2] + "\n")
        elif index == 2:
            texts += ('예금주 성명: ' + result[2] + "\n")
        else:
            texts += ('예금주 서명: ' + result[2] + "\n")
        index = index + 1
    # copy the result to clipboard, in order for AA to get te result back
    pyperclip.copy(texts)
    logging.info("final result: {}, {}".format(len(texts), texts.encode('utf-8').strip()))


def checkSignture(srcFileName, debug=False):
    logging.info(srcFileName)

    deskewedFileName, deskewedImg = correct_skew.deskewImage(srcFileName)
    logging.info("{}, {}".format(deskewedFileName, deskewedImg.shape))

    contourList = getcontour. getRectCoordinate(deskewedFileName, deskewedImg)
    logging.info("contours Selected {}".format(len(contourList)))

    checkResult = []
    for contour in contourList:
        ix, iy, iw, ih = cv2.boundingRect(contour)
        logging.info("Area to compare: {}, {}, {}, {}".format(ix, iy, iw, ih) )

        signatureROI = deskewedImg[iy+margin:iy+ih-margin, ix+margin:ix+iw-margin]
        ## cv2.imshow("Deskewed", deskewedImg)
        cv2.imshow(str(ix)+"SignatureROI", signatureROI)

        numNonBlack = cv2.countNonZero(signatureROI)
        whiteRate = numNonBlack / ((iw - (2 * margin)) * (ih - (2 * margin))) * 100
        logging.info("White rate(%): {:.3f}".format(whiteRate))

        resultText = '서명완료'
        if whiteRate >= SignWhiteRate:
            resultText = '미서명'

        checkResult.append([ix, whiteRate, resultText])

    del deskewedImg
    checkResult.sort()

    ## cv2.waitKey(0)
    cv2.destroyAllWindows()
    os.remove(deskewedFileName)
    genResult(checkResult)


if __name__ == '__main__':
    print('1')
    logging.basicConfig(filename='F:\\ws_py_windwos\\sli_signature\\venv\\checkSign.log', level=logging.DEBUG, format='%(asctime).19s:%(levelname).4s:%(module)-.10s(%(lineno)3d) %(message)s')

    logging.info("starting-------------------------------------")
    if len(sys.argv) == 1:
        print('2.1')
        logging.info("1..")
        # checkSignture("../images/hkli_image.png", True)
        # checkSignture("./images/hkli_image4of5.png", True)
        checkSignture("../images/hkli_skewed1_ppt.png", True)
        #checkSignture("../images/hkli_deskewed1.png", True)
    else:
        # construct the argument parse and parse the argumentss
        print('2.2')
        logging.info("2..")
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", required=True, help="path to input image file")
        args = vars(ap.parse_args())
        filename = args["image"]
        checkSignture(filename)
