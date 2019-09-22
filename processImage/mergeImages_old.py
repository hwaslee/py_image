import cv2
import numpy as np


image_names = ['/Volumes/USB-64/Image/emart/sub2.png', '/Volumes/USB-64/Image/emart/sub1.png']
images = []
max_width = 0           # find the max width of all the images
total_height = 0        # the total height of the images (vertical stacking)

for name in image_names:
    # open all images and find their sizes
    images.append(cv2.imread(name))

    # print(type(images[-1]), images[-1])
    # print(type(images[-1].shape), images[-1].shape)
    # print(type(images[-1].shape[1]), images[-1].shape[1])
    # print(1, type(images[-1]))
    # print(2, type(images[-1].shape))                          # <class, 'tuple'>, [0]:height, [1]:width, [2]:channel
    # print(3, type(images[-1].shape[0]), images[-1].shape[0])  # [0]:height, [1]:width, [2]:channel
    # print(4, type(images[-1].shape[1]), images[-1].shape[1])  # [1]:width

    # print(images[-1])
    if images[-1].shape[1] > max_width:
        max_width = images[-1].shape[1]
    total_height += images[-1].shape[0]

# create a new empty array with a size large enough to contain all the images
final_image = np.zeros((total_height, max_width, 3), dtype=np.uint8)

current_y = 0                   # keep track of where your current image was last placed in the y coordinate
for image in images:
    # add an image to the final array and increment the y coordinate
    final_image[current_y:current_y+image.shape[0], :image.shape[1], :] = image
    current_y += image.shape[0]

cv2.imwrite('/Volumes/USB3-64/Image/emart/fin.PNG', final_image)
print('done...')

