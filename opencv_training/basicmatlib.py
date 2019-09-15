import numpy as np
import cv2
import matplotlib.pyplot as plt

def showImage():
    imgfile = "/Volumes/USB3-64/ws_py/opencv_training/venv/images/watch.jpg"
    img = cv2.imread(imgfile, cv2.IMREAD_GRAYSCALE)

    plt.imshow(img, cmap='gray', interpolation='bicubic')
    plt.xticks([])
    plt.yticks([])
    plt.title("1st Work")
    plt.show()


showImage()
