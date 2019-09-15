import logging
# import re
import os
import sys

import cv2
import numpy as np
import pytesseract
from PIL import Image
import genResultExcelFile


SIGN_WHITERATE = 99.95
MARGIN = 2

# ------------------------------------------------------------------
# 원시Image, deskew용 contour에서 deskew된 image를 얻는다
# Input: 원시Image,
#        deskew용 contour
# Output: deskew된 Image
# ------------------------------------------------------------------
def deskewImage(fullImage, contour):
    logging.debug("fullImage: {}".format(fullImage.shape))

    ix, iy, iw, ih = cv2.boundingRect(contour)
    subImage = fullImage[iy-5:iy+ih+5, ix-5:ix+iw+5]
    cv2.imshow("SubImage", subImage)
    cv2.waitKey(0)
    logging.debug("subImage: {}".format(subImage.shape))

    gray = cv2.bitwise_not(subImage)

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    logging.debug("coords..{}".format(coords))
    angle = cv2.minAreaRect(coords)[-1]
    logging.info("angle: {:.5f}".format(angle))

    if abs(angle) != 0.0:
        logging.debug("Angle needs to be adjusted..")
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = fullImage.shape[:2]
        logging.info("height:{}, weight:{}".format(h, w))
        center = (w // 2, h // 2)
        middle = cv2.getRotationMatrix2D(center, angle, 1.0)
        ### rotated = cv2.warpAffine(image, middle, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        deskewedFull = cv2.warpAffine(fullImage, middle, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    else:
        deskewedFull = fullImage

    vis_r, vis_c = deskewedFull.shape
    cropped_resized = cv2.resize(deskewedFull, (int(vis_c / 2.5), int(vis_r / 2.5)))
    cv2.imshow(' Deskewed & Cropped_resized', cropped_resized)
    cv2.waitKey(0)

    del thresh
    del gray
    del subImage
    return deskewedFull


# ------------------------------------------------------------------
# 원시파일명에서 원시Image, deskew용 contour(정해진 영역에서의 최대 크기)를 얻는다
# Input: 원시파일명
# Output: 원시파일의 Image,
#         deskew용 contour
# 참고: cv2.RETR_EXTERNAL
# ------------------------------------------------------------------
def getImageInfoToDeskew(srcFilename):
    ### fullImage = cv2.imread(srcFilename, cv2.COLOR_BGR2GRAY)         # still 3 channels
    fullImage = cv2.imread(srcFilename)
    fullImage = cv2.cvtColor(fullImage, cv2.COLOR_BGR2GRAY)             # 2 channels
    ret, threshed = cv2.threshold(fullImage, 240, 255, cv2.THRESH_BINARY_INV)

    ex, ey, ew, eh = None, None, None, None

    # contours, hierarchy = cv2.findContours(threshed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count = 0;
    selectedContour = None
    selectedContour_size = 0.0
    logging.debug('How many EXTERNAL contours: {}'.format(len(contours)))

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
        count += 1

        if len(approx) == 4:
            contourSize = cv2.contourArea(contour)
            ix, iy, iw, ih = cv2.boundingRect(contour)
            if ix > 500 or iy > 1000 or contourSize < 5000 :
                 continue

            logging.debug("Contour matched [{}].. x:{}, y:{}, w:{}, h:{}, size:{}".format(count, ix, iy, iw, ih, contourSize))
            if selectedContour_size > contourSize:
                continue

            selectedContour = contour
            selectedContour_size = contourSize

    # exclude outer rectangle itself or smaller than threshold (width of the border line)
    # if ey == iy or abs(int(ew - iw)) > 10 or abs(int((ey + eh) - (iy + ih))) > 10:

    ### Duee to error, comment out
    ### cv2.drawContours(fullSrcImage, [selectedContour], -1, (0, 0, 255), 1)

    # resize cropped for visualization purposes only
    vis_r, vis_c = fullImage.shape
    cropped_resized = cv2.resize(fullImage, (int(vis_c/2.5), int(vis_r/2.5)))
    cv2.imshow(str(count) + ' Cropped_resized', cropped_resized)
    cv2.waitKey(0)

    del threshed
    del cropped_resized
    cv2.destroyAllWindows()
    return fullImage, selectedContour


# ------------------------------------------------------------------
# CCOMP mode에서 얻어진 Outer, Inner에서 유사하 것을 제거
# Input: selectedContours - 선택된 전체 contours info list
# Output: dedup contours info list
# ------------------------------------------------------------------
def dedupContours(selectedContours):
    dedupedContours = []

    pos_x = 10000
    pos_y = 10000
    for contInfo in selectedContours:
        dedupFlag = False
        for storedCont in dedupedContours:
            if abs(contInfo[0] - storedCont[0]) < 10 and abs(storedCont[1] - contInfo[1]) < 10:
                dedupFlag = True
                break

        if not dedupFlag:
            dedupedContours.append(contInfo)

    return dedupedContours


# ------------------------------------------------------------------
# Image 에서 적절한 모든 contour 정보 list 를 얻는다
# Input: Image - deskewed Image
# Output: contours
# 참고: cv2.RETR_CCOMP
# ------------------------------------------------------------------
def getContourInfos(deskewedImage):
    fullImage = deskewedImage.copy()
    ret, threshed = cv2.threshold(fullImage, 240, 255, cv2.THRESH_BINARY_INV)

    ex, ey, ew, eh = None, None, None, None

    contours, hierarchy = cv2.findContours(threshed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # contours, hierarchy = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count = 0;
    selectedContours = []
    #selectedContour_size = 0.0
    logging.info('How many CCOMP contours: {}'.format(len(contours)))
    for contour in contours:

        approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
        count += 1

        if len(approx) == 4:
            contourSize = cv2.contourArea(contour)
            ix, iy, iw, ih = cv2.boundingRect(contour)
            if ix  == 0 or iy == 0 or contourSize < 5000 :
                 continue

            logging.debug("Contour matched [{}].. x:{}, y:{}, w:{}, h:{}, size:{}".format(count, ix, iy, iw, ih, contourSize))

            cv2.drawContours(fullImage, [contour], -1, (0, 0, 255), 1)

            selectedContours.append([ix, iy, iw, ih, contourSize])

    selectedContours.sort(reverse=True)
    logging.debug('--------------------------')
    idx = 0
    for contInfo in selectedContours:
        logging.debug("{}, {}, {}, {}, {}, {}".format(idx, contInfo[0], contInfo[1], contInfo[2], contInfo[3], contInfo[4]))
        idx += 1
    logging.debug('--------------------------')

    selectedContours = dedupContours(selectedContours)

    idx = 0
    for contInfo in selectedContours:
        logging.info("{}, {}, {}, {}, {}, {}".format(idx, contInfo[0], contInfo[1], contInfo[2], contInfo[3], contInfo[4]))
        idx += 1
    logging.debug('--------------------------')

    # resize cropped for visualization purposes only
    vis_r, vis_c = fullImage.shape
    cropped_resized = cv2.resize(fullImage, (int(vis_c/2.5), int(vis_r/2.5)))
    cv2.imshow(str(count) + ' Cropped_resized', cropped_resized)
    cv2.waitKey(0)

    del threshed
    del fullImage
    cv2.destroyAllWindows()
    return selectedContours


# ------------------------------------------------------------------
# 검색된 contours 에서 keyword에서 명시한 contour를 얻는다
# Input: contours - 검색된 contours,
#        keyword - 영역을 정의하는 keyword
# Output: contours
# ------------------------------------------------------------------
def getConturImage(contours, keyword):
    if keyword == 'desno':
        return contours[-1]
    elif keyword == 'custid':
        return contours[-2]
    # select contours with pos_y close to max of pos_y
    elif keyword == 'sign':
        retCont = []
        max = 0
        for cont in contours:
            if cont[1] > max:
                max = cont[1]
        for cont in contours:
            if abs(cont[1] - max) < 10:
                retCont.append(cont)
        return retCont
    else:
        logging.debug("Wrong keyword")

'''
def getConditionalContours(deskewedFullImage, option):
    # Hwa: image with 2 channels passed, so don't need to call cvtColor to make it gray
    # image = cv2.imread(fileName)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Hwa: With threshold of 240, successful to get coord of rectangle using contour in case of poor quality of image
    ret, threshed = cv2.threshold(deskewedFullImage, 240, 255, cv2.THRESH_BINARY_INV)

    ex, ey, ew, eh = None, None, None, None

    # contours, hierarchy = cv2.findContours(threshed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count = 0;
    contourList = []
    logging.debug('How many contours: {}'.format(len(contours)))
    for contour in contours:

        approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
        count += 1

        if len(approx) == 4:
            contourSize = cv2.contourArea(contour)
            ix, iy, iw, ih = cv2.boundingRect(contour)
            if ix ==0 or iy ==0 or contourSize < 10000 :
                continue

            logging.debug("Contour matched [{}].. x:{}, y:{}, w:{}, h:{}, size:{}".format(count, ix, iy, iw, ih, contourSize))

            # exclude outer rectangle itself or smaller than threshold (width of the border line)
            # if ey == iy or abs(int(ew - iw)) > 10 or abs(int((ey + eh) - (iy + ih))) > 10:
            cv2.drawContours(deskewedFullImage, [contour], -1, (0, 0, 255), 1)

            # resize cropped for visualization purposes only
            vis_r, vis_c = deskewedFullImage.shape
            cropped_resized = cv2.resize(deskewedFullImage, (int(vis_c/2.5), int(vis_r/2.5)))
            cv2.imshow(str(count) + ' Cropped_resized', cropped_resized)

    del threshed
    cv2.waitKey(0)
    cv2.destroyAllWindows()
'''

# ------------------------------------------------------------------
# image 에서 Tesseract OCR 인식하여 text를 얻는다
# Input: image - 영역 image
#        offset - image에서 처리할 x-axis offset
# Output: OCR 인식한 text
# ------------------------------------------------------------------
def getTextFromSubimage(image, offset):
    cv2.imwrite("subImage.png", image[:, offset:])
    try:
        ### ocr_text = pytesseract.image_to_string(Image.open("subImage.png"), lang='kor')
        ocr_text = pytesseract.image_to_string(Image.open("subImage.png"))
        logging.info("OCR TEXT: [{}]".format(ocr_text))
        '''
        regex = re.compile(':\s{*}\d{*}$')
        matchobj = regex.search(ocr_text)
        value = matchobj.group(0)
        '''
        os.remove("subImage.png")
        return ocr_text
    except:
        logging.exception("exception while getting text ")
        os.remove("subImage.png")
        return '-'


# ------------------------------------------------------------------
# image 에서 서명 부분을 인식하여 white pixel 비율을 얻는다
# Input: image - 영역 image
#        signConts - 서명영역 contour list
# Output: 각 서명란의 점검 결과 list ('O', 'X', '-')
# ------------------------------------------------------------------
def checkSignture(deskewedFull, signConts):
    # rel_X, rel_Y, contourList = getcontour.getRectCoordinate(fullImage)
    # logging.debug("contours Selected {}".format(len (contourList)))

    checkResult = ['-', '-', '-', '-']
    idx = 0
    for signCont in signConts:
        signROI = deskewedFull[signCont[1] + MARGIN : signCont[1] + signCont[3] - MARGIN,
                               signCont[0] + MARGIN : signCont[0] + signCont[2] - MARGIN]
        logging.info("signROI shape: {}".format(str(signROI.shape)))
        ### cv2.cvtColor(signROI, cv2.COLOR_BGR2GRAY)           # already 2 channels
        signROI = cv2.threshold(signROI, 200, 255, cv2.THRESH_BINARY)[1]
        cv2.imshow(str(idx) + " Signature", signROI)

        logging.info("contour: {}".format(signConts))
        logging.debug(signROI)

        numOfWhite = cv2.countNonZero(signROI)
        totCell = (signCont[2] - (2 * MARGIN)) * (signCont[3] - (2 * MARGIN))
        whiteRate = numOfWhite / totCell * 100
        logging.info("White:{}, totCell:{}, White %:{}".format(numOfWhite, totCell, whiteRate))

        if whiteRate >= SIGN_WHITERATE:
            checkResult[idx] = 'X'
        else:
            checkResult[idx] = 'O'

        idx += 1

    logging.info("sign exists? {}".format(checkResult))
    return checkResult


# ------------------------------------------------------------------
# 인식 결과를 엑셀에 저장한다
# Input: desNo - Design No
#        custId - Customer Id
#        results - 서명부분 인식 결과 list
#        srcFilename - 이미지파일명
# Output: -
# 참고: Excel 파일명은 엑셀 module 안에 지정되어 있음
# ------------------------------------------------------------------
def genExcelResult(desNo, custId, results, srcFilename):
    genResultExcelFile.initExcelFile()
    genResultExcelFile.writeToExcel(desNo, custId, results, srcFilename)



if __name__ == '__main__':
    logging.basicConfig(filename='..\log\getDeskewedTest.log', level=logging.INFO, format='%(asctime).19s:%(levelname).4s:%(module)-.10s(%(lineno)3d) %(message)s')
    logging.info("------------ new starting -------------------------------------")

    if len(sys.argv) == 1:
        # folder = sys.argv[1]
        folder = "F:\Image\HKFMI"
        for eachFile in os.listdir(folder):
            filename = os.path.join(folder, eachFile)
            logging.debug(filename)

            if not os.path.isfile(filename):
                logging.debug('{} is directory'.format(filename))
                continue

            if filename.split(".")[-1] != 'png' and filename.split(".")[-1] != 'jpg':
                continue

            logging.info("--- Image file {} will be analyzed".format(filename))

            fullImage, rectContour = getImageInfoToDeskew(filename)
            deskewedFull = deskewImage(fullImage, rectContour)
            del fullImage
            allContours = getContourInfos(deskewedFull)
            logging.debug("len(Contours) selected: {}".format(len(allContours)))

            desNoCont = getConturImage(allContours, "desno")
            desNoImage = deskewedFull[desNoCont[1]:desNoCont[1]+desNoCont[3], desNoCont[0]:desNoCont[0]+desNoCont[2]]
            cv2.imshow("Design No", desNoImage)
            cv2.waitKey(0)
            desnoText = getTextFromSubimage(desNoImage, 150)

            custidCont = getConturImage(allContours, "custid")
            custidImage = deskewedFull[custidCont[1]:custidCont[1]+custidCont[3], custidCont[0]:custidCont[0]+custidCont[2]]
            cv2.imshow("Cust ID", custidImage)
            cv2.waitKey(0)
            custidText = getTextFromSubimage(custidImage, 150)

            logging.debug("After OCR, Des NO:{}, Cust ID:{}".format(desnoText, custidText))

            signConts = getConturImage(allContours, "sign")
            signConts.sort()
            logging.debug("Signature Contours: {}".format(len(signConts)))
            checkResult = checkSignture(deskewedFull, signConts)

            genExcelResult(desnoText, custidText, checkResult, filename)

            del deskewedFull

            cv2.waitKey(0)
            cv2.destroyAllWindows()

        logging.debug("end of directory..")