# main program to check if signature exists or not for SLI
#
import numpy as np
import cv2
import os
import sys
# import pyperclip
import logging
from os import listdir
from os.path import isfile, join
from PIL import Image
import pytesseract
import correct_skew
import getcontour
import re
import genResultExcelFile


'''
## To use specific logger instead of root logger
## Need to elaborate more

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
SignWhiteRate = 99.7

global fullImage

def genExcelResult(desNo, custId, results, srcFilename):
    genResultExcelFile.initExcelFile()
    genResultExcelFile.writeToExcel(desNo, custId, results, srcFilename)
    '''
    ## To copy the result to clipboard

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
    '''


def getTextFromSubimage(fullImage):
    desNo = None
    custId = None

    desNoImg = fullImage[400:510, 250:570]
    cv2.imshow("Design No", desNoImg)
    cv2.waitKey(0)

    try:
        cv2.imwrite("subImage.png", desNoImg)
        ### desNo = pytesseract.image_to_string(Image.open("subImage.png"), lang='kor')
        desNo = pytesseract.image_to_string(Image.open("subImage.png"))
        logging.info("OCR Design No: [{}]".format(desNo))
        regex = re.compile('ID:\s{*}\d{*}$')
        matchobj = regex.search(desNo)
        desNo = matchobj.group(0)
        logging.info("Design NO: {}".format(desNo))
        os.remove("subImage.png")
    except:
        logging.exception("exception while getting DesignNo ")
        return desNo, custId

    try:
        custIdImg = fullImage[510:580, 250:570]
        cv2.imshow("Cust ID", custIdImg)
        cv2.waitKey(0)
        cv2.imwrite("subImage.png", custIdImg)
        ### custId = pytesseract.image_to_string(Image.open("subImage.png"), lang='kor')
        custId = pytesseract.image_to_string(Image.open("subImage.png"))
        logging.info("OCR Cust ID: {}".format(custId))
        regex = re.compile('\d{*}$')
        matchobj = regex.search(custId)
        custId = matchobj.group(0)
        logging.info("Cust ID: {}".format(custId))
        os.remove("subImage.png")
    except:
        logging.exception("exception while getting DesignNo")

    return desNo, custId


def getIDfromFile(fullImage):
    subImage = fullImage[200:550, 130:550]
    cv2.imshow("Design-NO & Cust-ID", subImage)
    cv2.waitKey(0)

    deskewedImg = correct_skew.deskewImage(fullImage, subImage)
    cv2.imshow("Checking... skewed ..", deskewedImg)
    cv2.waitKey(0)

    del subImage

    desNo, custId = getTextFromSubimage(deskewedImg)
    return deskewedImg, desNo, custId


def checkSignture(fullImage, desNo, custId, srcFilename):
    rel_X, rel_Y, contourList = getcontour.getRectCoordinate(fullImage)
    logging.info("contours Selected {}".format(len(contourList)))

    checkResult = []
    for contour in contourList:
        ix, iy, iw, ih = cv2.boundingRect(contour)
        ### logging.info("Area to compare: {}, {}, {}, {}".format(ix, iy, iw, ih) )

        signatureROI = fullImage[rel_Y+iy+margin:rel_Y+iy+ih-margin, rel_X+ix+margin:rel_X+ix+iw-margin]
        ## cv2.ims how("Deskewed", deskewedImg)
        cv2.imshow(str(ix)+"SignatureROI", signatureROI)

        numNonBlack = cv2.countNonZero(signatureROI)
        whiteRate = numNonBlack / ((iw - (2 * margin)) * (ih - (2 * margin))) * 100

        resultText = 'O'
        if whiteRate >= SignWhiteRate:
            resultText = 'X'

        logging.info("File:{}, result:{}, White rate(%): {:.3f}".format(srcFilename, resultText, whiteRate))
        checkResult.append([ix, whiteRate, resultText])

    del fullImage
    checkResult.sort()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    genExcelResult(desNo, custId, checkResult, srcFilename)


if __name__ == '__main__':
    logging.basicConfig(filename='..\log\checkSign_folder.log', level=logging.DEBUG, format='%(asctime).19s:%(levelname).4s:%(module)-.10s(%(lineno)3d) %(message)s')
    logging.info("------------ new starting -------------------------------------")

    if len(sys.argv) == 1:
        # folder = sys.argv[1]
        folder = "F:\Image\HKFMI"
        fullname = ''
        for eachFile in listdir(folder):
            fullname = join(folder, eachFile)
            logging.debug(fullname)
            if not isfile(fullname):
                logging.debug('{} is directory'.format(fullname))
                continue

            if fullname.split(".")[-1] != 'png' and fullname.split(".")[-1] != 'jpg':
                continue

            logging.debug('{} is file......'.format(eachFile))
            fullImage = cv2.imread(fullname, cv2.COLOR_BGR2GRAY)
            fullImage, desNo, custId = getIDfromFile(fullImage)
            logging.info("Design No:{}, Cust ID:{}".format(desNo, custId))
            checkSignture(fullImage, desNo, custId, eachFile)

        logging.info("end of directory..")

