import numpy as np
import cv2


def applyAdaptiveThreshold():
    print ('--------- color 이미지 속성 -----------')



    titles = ['../images/KakaoTalk_Photo_2018-12-31-08-25-25.jpeg', '../images/KakaoTalk_Photo_2018-12-31-08-25-36.jpeg']


    for i in range(2):
        img = cv2.imread(titles[i])
        img = cv2.resize(img, (600, 900))
        cv2.imshow(titles[i], img)
        cv2.imwrite(titles[i], img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


applyAdaptiveThreshold()