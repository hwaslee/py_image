#
import cv2



# img = cv2.imread('../images/deskewedSignature1_28170519.png')
img = cv2.imread('../images/deskewed.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

det = cv2.createLineSegmentDetector()
det.detect(gray, lines)
