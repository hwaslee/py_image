import cv2
import numpy as np


original = cv2.imread("a.jpg")
duplicate = cv2.imread("b.jpg")

if original.shape == duplaicate.shape:
    print("smae size and channels")

    difference = cv2.subtract(orignal, duplicate)
    b, g, r = cv2.split(difference)

    cv2.imshow("difference", b)

    if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
        print("completely equal")

cv2.imshow("original", original)
cv2.imshow("duplicate", duplicate)
cv2.waitKey(0)
cv2.destroyAllWindows()

