from PIL import Image
from pytesseract import *
from datetime import datetime


pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/4.0.0/bin/tesseract'

def OCR(imgfile, lang='eng'):
    stime = datetime.now()

    im = Image.open(imgfile)
    text = pytesseract.image_to_string(im, lang=lang)
    print(text)

    etime = datetime.now()
    duration = etime - stime
    print("time elapsed: {:.2f} secs".format(duration.total_seconds()))

# OCR('../images/ocr_data.png')                       # x
# OCR('../images/ocr_data.png', lang='kor_1')         # 나름 OK
# OCR('../images/ocr_data.png', lang='kor_2')         # 나름 OK
# OCR('../images/ocr_data.png', lang='kor_3')         # 나름 OK
# OCR('../images/ocr_data.png', lang='kor_vert1')     # x
# OCR('../images/ocr_data.png', lang='kor_vert2')     # x
# OCR('../images/ocr_data.png', lang='kor_vert3')     # x
# OCR('../images/ocr_data.png', lang='Hangul')        # 나름 OK
# OCR('../images/ocr_data.png', lang='Hangul_vert')   # x

# OCR('../images/deskewed.png')                       # x
# OCR('../images/deskewed.png', lang='kor_1')         # 나름 OK
# OCR('../images/deskewed.png', lang='kor_2')         # 나름 OK
OCR('../images/deskewed.png', lang='kor_3')         # 나름 OK
# OCR('../images/deskewed.png', lang='kor_vert1')     # x
# OCR('../images/deskewed.png', lang='kor_vert2')     # x
# OCR('../images/deskewed.png', lang='kor_vert3')     # x
# OCR('../images/deskewed.png', lang='Hangul')        # x
# OCR('../images/deskewed.png', lang='Hangul_vert')   # x