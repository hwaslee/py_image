import cv2
import sys
import pytesseract
from datetime import datetime

fileName = ''

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python3 textDetectionUsingTesseract.py <filename> <lang>')
        sys.exit(1)

    sys.path.append('..\\util')
    print(sys.path)
    import sysutil

    tick = datetime.now()
    # filename is specified
    imPath = sys.argv[1]            # 'F:\\Image\\images\\OCR_Test.png'

    # Read image path from command line
    trainedLang = sys.argv[2]        # 'eng+kor'

    # Uncomment the line below to provide path to tesseract manually
    # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

    # Define config parameters.
    # '-l eng'  for using the English language
    # '--oem 1' for using LSTM OCR Engine
    config = ('-l ' + trainedLang +  ' --oem 1 --psm 3')

    # Read image from disk
    #  im = cv2.imread(imPath, cv2.IMREAD_COLOR)
    im = cv2.imread(imPath, cv2.IMREAD_GRAYSCALE)

    # Run tesseract OCR on image
    texts = pytesseract.image_to_string(im, config=config)

    # Print recognized text
    print(texts)
    sysutil.copy2clip(texts)

    tock = datetime.now()
    duration = tock - tick
    print("time elapsed: {:.2f} secs".format(duration.total_seconds()))


