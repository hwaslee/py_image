# USAGE
# python correct_skew.py --image images/neg_28.png


import numpy as np
import argparse
import cv2
import os
import sys
from datetime import datetime


def getDeskewedFilename(srcName, id=None):
	filename_w_ext = os.path.basename(srcName)
	filename, file_extension = os.path.splitext(filename_w_ext)
	hms = datetime.now().strftime('%d%H%M%S')
	if id != None:
		newName = srcName.replace(filename, 'de'+filename+"_"+id+"_"+hms)
	else:
		newName = srcName.replace(filename, 'de'+filename+"_"+hms)
	return newName


def deskewImage(fileName):
	image = cv2.imread(fileName)
	print("2,", fileName, image)

	# convert the image to grayscale and flip the foreground
	# and background to ensure foreground is now "white" and
	# the background is "black"
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.bitwise_not(gray)

	# threshold the image, setting all foreground pixels to 255 and all background pixels to 0
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	cv2.imwrite(getDeskewedFilename(fileName, "thresh"), thresh)

	# grab the (x, y) coordinates of all pixel values that
	# are greater than zero, then use these coordinates to
	# compute a rotated bounding box that contains all
	# coordinates
	coords = np.column_stack(np.where(thresh > 0))
	angle = cv2.minAreaRect(coords)[-1]
	print("angle: {}".format(angle))

	# the `cv2.minAreaRect` function returns values in the
	# range [-90, 0); as the rectangle rotates clockwise the
	# returned angle trends to 0 -- in this special case we
	# need to add 90 degrees to the angle
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

	# save rotated image to new file
	cv2.imwrite(getDeskewedFilename(fileName), rotated)
	height, width, channels = rotated.shape
	print("Heiht:{}, Width:{}, Channels:{}".format(height, width, channels))
	dim2 = rotated.reshape(channels, height, width)
	print(dim2)

	# draw the correction angle on the image so we can validate it
	cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

	# show the output image
	print("[INFO] angle: {:.5f}".format(angle))
	cv2.imshow("Input", image)
	cv2.imshow("Rotated", rotated)

	# cv2.waitKey(0)


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print ("1.", sys.argv)
		# deskewImage("../images/skewedSignature1.png")

		# deskewImage("../images/notapproved/surin.jpg")
		# deskewImage("../images/notapproved/제이제이스포츠_사업자정보변경신청서.jpg")
		# deskewImage("../images/notapproved/파타티_간이과세자.jpg")
		deskewImage("../images/notapproved/헬로홈케어_간이과세자.JPG")
		deskewImage("../images/approved/리빙메이드_일반과세자.JPG")
		deskewImage("../images/approved/성현산업(주)_법인사업자.jpg")
		deskewImage("../images/approved/아이니새싹삼_부가가치세 면세사업자.jpg")
		deskewImage("../images/approved/영어조합법인 _면제법인사업자.jpg")
		deskewImage("../images/approved/우진인터비젼_공동대표자_법인사업자.JPG")
		deskewImage("../images/approved/장항세계롤협동조합_면세법인사업자.jpg")
		deskewImage("../images/approved/코몽드_일반과세자.jpg")
		deskewImage("../images/approved/허밍아비스_ 법인사업자.jpg")

	else:
		# construct the argument parse and parse the argumentss
		ap = argparse.ArgumentParser()
		ap.add_argument("-i", "--image", required=True, help="path to input image file")
		args = vars(ap.parse_args())
		filename = args["image"]
		deskewImage(filename)