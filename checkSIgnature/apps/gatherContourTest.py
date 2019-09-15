# 실제 이미지에서 직사각형으로부터 처리 영역을 확인하기 위하여
# 전체 이미지에서 크기가 10,000 이상인 직사각형의 좌표를 찾는 방법.
import numpy as np
import cv2
import sys
import logging


def deskewImage(fullImage, subImage):
    # cv2.imshow("Original", image)
    # logging.info("Image...\n", image)
    ret, image = cv2.threshold(subImage, 170, 255, cv2.THRESH_BINARY)
    ## cv2.imshow("Original after threshold", image)
    ## cv2.waitKey(0)

    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    gray = cv2.cvtColor(subImage, cv2.COLOR_BGR2GRAY)
    # logging.info("\nGray...\n", gray)
    gray = cv2.bitwise_not(gray)
    ## cv2.imshow("Gray", gray)
    ## cv2.waitKey(0)

    # threshold the image, setting all foreground pixels to 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    ### thresh = cv2.threshold(subImage, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # logging.info("Thresh...\n", thresh)
    ## cv2.imshow("Thresh", thresh)
    ## cv2.waitKey(0)

    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    # logging.info("np.where....\n", np.where(thresh > 0))
    coords = np.column_stack(np.where(thresh > 0))
    logging.info("coords..{}".format(coords))
    angle = cv2.minAreaRect(coords)[-1]
    logging.info("angle: {}".format(angle))

    '''
    logging.info('----------------------------')
    cntrs, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cntr in cntrs:
        approx = cv2.approxPolyDP(cntr, 0.01 * cv2.arcLength(cntr, True), True)

        if len(approx) == 4 and cv2.contourArea(cntr) > 10:
            logging.info("size: ", cv2.contourArea(cntr))
            cv2.drawContours(image, [cntr], -1, (0, 0, 255), 1)
            cv2.imshow('Contour selected', image)
            cv2.waitKey(0)
    logging.info('----------------------------')
    '''

    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    logging.info("[INFO] angle: {:.5f}".format(angle))
    if abs(angle) != 0.0:
        logging.info("Angle needs to be adjusted..")
        if angle < -45:
            angle = -(90 + angle)

        # otherwise, just take the inverse of the angle to make
        # it positive
        else:
            angle = -angle

        # rotate the image to deskew it
        ### (h, w) = image.shape[:2]
        (h, w) = fullImage.shape[:2]
        logging.info("height:{}, weight:{}".format(h, w))
        center = (w // 2, h // 2)
        middle = cv2.getRotationMatrix2D(center, angle, 1.0)
        ### rotated = cv2.warpAffine(image, middle, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        deskewedFull = cv2.warpAffine(fullImage, middle, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        deskewedFull = cv2.cvtColor(deskewedFull, cv2.COLOR_BGR2GRAY)
    else:
        deskewedFull = fullImage
        deskewedFull = cv2.cvtColor(deskewedFull, cv2.COLOR_BGR2GRAY)

    '''
    # save rotated image to new file
    deskewedFileName = getDeskewedFilename(filename)
    cv2.imwrite(deskewedFileName, rotated)
    '''

    # height, width, channels = rotated.shape
    # height, width = deskewedFull.shape
    # logging.info("Heiht:{}, Width:{}, Channels:{}".format(height, width, channels))
    # dim2 = rotated.reshape(channels, height, width)
    # logging.info(dim2)

    # draw the correction angle on the image so we can validate it
    # cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # cv2.imshow("Input", image)
    cv2.imshow("Deskewed FullImage", deskewedFull)
    cv2.waitKey(0)

    '''
    Should have some logic to avoid memory leak.... like below
    '''
    # thresh.release()
    # gray.release()
    # image.release()\
    del thresh
    del gray
    del image
    return deskewedFull


def gatherRectCoordinate(deskewedFullImage):
    # Hwa: image with 2 channels passed, so don't need to call cvtColor to make it gray
    # image = cv2.imread(fileName)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Hwa: With threshold of 240, successful to get coord of rectangle using contour in case of poor quality of image
    ret, threshed = cv2.threshold(deskewedFullImage, 240, 255, cv2.THRESH_BINARY_INV)

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
    for contour in contours:

        approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
        count += 1

        if len(approx) == 4:
            contourSize = cv2.contourArea(contour)
            ix, iy, iw, ih = cv2.boundingRect(contour)
            if ix ==0 or iy ==0 or contourSize < 10000 :
                continue

            logging.info("Contour matched [{}].. x:{}, y:{}, w:{}, h:{}, size:{}".format(count, ix, iy, iw, ih, contourSize))

            # exclude outer rectangle itself or smaller than threshold (width of the border line)
            # if ey == iy or abs(int(ew - iw)) > 10 or abs(int((ey + eh) - (iy + ih))) > 10:
            cv2.drawContours(deskewedFullImage, [contour], -1, (0, 0, 255), 3)

            # resize cropped for visualization purposes only
            vis_r, vis_c = deskewedFullImage.shape
            cropped_resized = cv2.resize(deskewedFullImage, (int(vis_c/2.5), int(vis_r/2.5)))
            cv2.imshow(str(count) + ' Cropped_resized', cropped_resized)

    del threshed
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    logging.basicConfig(filename='..\log\gatherContours.log', level=logging.DEBUG, format='%(asctime).19s:%(levelname).4s:%(module)-.10s(%(lineno)3d) %(message)s')

    if len(sys.argv) == 1:
        # filename = "F:\Image\HKFMI\sample.png"
        # filename = "F:\Image\HKFMI\Scan0021.jpg"
        filename = "F:\Image\HKFMI\Scan0022.jpg"
        # filename = "F:\Image\HKFMI\Scan0023.jpg"

    else:
        filename = sys.argv[1]

    logging.info("----- Image file {} will be analyzed ----------------".format(filename))

    fullImage = cv2.imread(filename, cv2.COLOR_BGR2GRAY)
    subImage = fullImage[200:550, 130:550]      # -61
    # subImage = fullImage[300:600, 130:600]    # -0.0
    cv2.imshow("Sample area", subImage)
    cv2.waitKey(0)

    deskewedFull = deskewImage(fullImage, subImage)
    gatherRectCoordinate(deskewedFull)
    # x, y, w, h = cv2.boundingRect(contour)
    # logging.info("Signature contour found.. x:{}, y:{}, w:{}, h:{}".format(x, y, w, h))
    cv2.destroyAllWindows()
