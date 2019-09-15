# USAGE
# python correct_skew.py --image images/neg_28.png


import numpy as np
import argparse
import cv2
import os
import sys
from datetime import datetime
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


def getDeskewedFilename(srcName, id=None):
	filename_w_ext = os.path.basename(srcName)
	filename, file_extension = os.path.splitext(filename_w_ext)
	hms = datetime.now().strftime('%d%H%M%S')
	if id != None:
		newName = srcName.replace(filename, 'de'+filename+"_"+id+"_"+hms)
	else:
		newName = srcName.replace(filename, 'de'+filename+"_"+hms)
	return newName


def deskewImage(filename):
	logging.info(filename)
	try:
		image = cv2.imread(filename)
	except:
		logging.exception("message")

	# cv2.imshow("Original", image)
	# logging.info("Image...\n", image)
	ret, image = cv2.threshold(image, 170, 255, cv2.THRESH_BINARY)
	# cv2.imshow("Original after threshold", image)

	# convert the image to grayscale and flip the foreground
	# and background to ensure foreground is now "white" and
	# the background is "black"
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# logging.info("\nGray...\n", gray)
	gray = cv2.bitwise_not(gray)
	# cv2.imshow("Gray", gray)

	# threshold the image, setting all foreground pixels to 255 and all background pixels to 0
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	# logging.info("Thresh...\n", thresh)
	# cv2.imshow("Thresh", thresh)

	# cv2.waitKey(0)

	# grab the (x, y) coordinates of all pixel values that
	# are greater than zero, then use these coordinates to
	# compute a rotated bounding box that contains all
	# coordinates
	# logging.info("np.where....\n", np.where(thresh > 0))
	coords = np.column_stack(np.where(thresh > 0))
	# logging.info("coords..\n", coords)
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
	if abs(angle) != 0.0:
		logging.info("Angle needs to be adjusted..")
		if angle < -45:
			angle = -(90 + angle)

		# otherwise, just take the inverse of the angle to make
		# it positive
		else:
			angle = -angle

	# rotate the image to deskew it
	(h, w) = image.shape[:2]
	center = (w // 2, h // 2)
	middle = cv2.getRotationMatrix2D(center, angle, 1.0)
	rotated = cv2.warpAffine(image, middle, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

	rotated = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)

	'''
	# save rotated image to new file
	deskewedFileName = getDeskewedFilename(filename)
	cv2.imwrite(deskewedFileName, rotated)
	'''

	# height, width, channels = rotated.shape
	height, width = rotated.shape
	# logging.info("Heiht:{}, Width:{}, Channels:{}".format(height, width, channels))
	# dim2 = rotated.reshape(channels, height, width)
	# logging.info(dim2)

	# draw the correction angle on the image so we can validate it
	# cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

	# show the output image
	logging.info("[INFO] angle: {:.5f}".format(angle))
	# cv2.imshow("Input", image)
	cv2.imshow("Deskewed", rotated)
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
	return deskewedFileName, rotated


if __name__ == '__main__':
	if len(sys.argv) == 1:
		# deskewImage("../images/hkli_image4of5-2.png")
		# deskewImage("../images/hkli_image1of5-1.png")
		# deskewImage("../images/hkli_image1of5-2.png")
		# deskewImage("../images/hkli_deskewed1.png")
		deskewImage("../images/hkli_skewed1_ppt.png")
	else:
		# construct the argument parse and parse the argumentss
		ap = argparse.ArgumentParser()
		ap.add_argument("-i", "--image", required=True, help="path to input image file")
		args = vars(ap.parse_args())
		filename = args["image"]
		deskewImage(filename)