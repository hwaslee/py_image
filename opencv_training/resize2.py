import numpy as np
import cv2 as cv
import copy

original = cv.imread("/Volumes/USB3-64/Image/HKFMI/deskewedImage.png", cv.IMREAD_UNCHANGED)

# resize original for visualization purposes only
print('original {}'.format(original.shape))
original_resized = cv.resize(original, (0,0), fx=.1, fy=.1)
cv.imshow('original_resize',original_resized)


img_resize = cv.resize(original, (0,0), fx=.9, fy=.9)

rows,cols = img_resize.shape
M = np.float32([[1,0,100],[0,1,50]])
offset_image = cv.warpAffine(img_resize,M,(cols,rows))

crop_img = offset_image[0:1080, 0:1920].copy()

print('img_resize {}'.format(img_resize.shape))
print('offset_image {}'.format(offset_image.shape))
print('cropped {}'.format(crop_img.shape))


# resize cropped for visualization purposes only
vis_r,vis_c = original_resized.shape
cropped_resized = cv.resize(crop_img, (vis_c, vis_r))
cv.imshow('cropped_resized',cropped_resized)


# cv.imshow('image',crop_img)

cv.waitKey(0)
cv.destroyAllWindows()