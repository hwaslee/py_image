# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/vision/cloud-client/detect/detect.py
import io
from datetime import datetime
from google.cloud import vision
# import sysutil
import sys
sys.path.insert(1, '/Users/andrew/Documents/py_basic/util')
import timeutil


class OCRHandler:
    def __init__(self):
        self.elapsed = 0
        self.filename = ''

    # GCV를 이용하여 local file에 대한 OCR 인식을 처리
    # Input: image filename
    # Output: 형태소 관련 정보 list
    def detect_text(self, file):
        ocr_time = timeutil.TimeElapsed()
        words_list = []

        tick = datetime.now()
        """Detects text in the file."""
        client = vision.ImageAnnotatorClient()
        sys.path.append('../util')
        # sys.path.append('..\\util')
        # print(sys.path)

        # [START vision_python_migration_text_detection]
        with io.open(file, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations

        # for text in texts:
        #     print("{}".format(text.description))
        #     sysutil.copy2clip(text.description)
        #     pyperclip.copy(text.description)
        #     break;

        index = 0
        for text in texts:
            index += 1

            # 방법 1: vertext 정보를 list로 변환하여 return
            # print(text.description, text.bounding_poly.vertices)
            # print(type(text.description), type(text.bounding_poly.vertices))
            # print('"{} [{:>15s}]"'.format(index, text.description))

            vertices = [[int(vertex.x), int(vertex.y)]
                        for vertex in text.bounding_poly.vertices]

            temp = [text.description, vertices]

            # 방법 2: 직접 generator object를 return, 사용할 때 철가 필요
            # print(text.description, text.bounding_poly.vertices)
            # print(type(text.description), type(text.bounding_poly.vertices))
            # print('"{} [{:>15s}]"'.format(index, text.description))
            # vertices = ('[{},{}]'.format(int(vertex.x), int(vertex.y))
            #             for vertex in text.bounding_poly.vertices)

            words_list.append(temp)

        print("Time to spend for OCR 인식", ocr_time.getelapsed())
        return words_list

    # def get_single_word(self, text):
    #     temp = []
    #     print(text.description)
    #     temp.append
    #     return  NULL

    # def detect_text_uri(self, uri):
    #     tick = datetime.now()
    #     """Detects text in the file located in Google Cloud Storage or on the Web.
    #     """
    #     # from google.cloud import vision
    #     client = vision.ImageAnnotatorClient()
    #     image = vision.types.Image()
    #     image.source.image_uri = uri
    #
    #     response = client.text_detection(image=image)
    #     texts = response.text_annotations
    #     print('Type(texts):', type(texts))
    #     print('Texts:', texts)
    #     print('--------------------')
    #     # sysutil.copy2clip(texts)
    #
    #     for text in texts:
    #         print('\n"{}"'.format(text.description))
    #
    #         vertices = (['({},{})'.format(vertex.x, vertex.y)
    #                     for vertex in text.bounding_poly.vertices])
    #
    #         print('bounds: {}'.format(','.join(vertices)))
    #
    #     tock = datetime.now()
    #     duration = tock - tick
    #     print("time elapsed: {:.2f} secs".format(duration.total_seconds()))


if __name__ == '__main__':
    '''
    if len(sys.argv) < 2:
        print('Usage: python3 textDetectionUsingGCV.py <filename>')
        sys.exit(1)

    detect_text(sys.argv[1])
    '''
    # filename = '/Volumes/USB3-64/Image/transaction.PDF'
    # filename = '/Volumes/USB3-64/Image/10167389_1.jpg'

    # filename = '/Volumes/USB3-64/Image/1. 10160920 다나한 인삼잎 보윤 수분크림.jpg'
    # filename = '/Volumes/USB3-64/Image/2. 10160902 참존 마유 골든컴플렉스 2종 세트.png'
    # filename = '/Volumes/USB3-64/Image/3. 10164315  쁘띠프루티 울트라 모이스처라이징 페이셜 마스크팩.jpg'
    # filename = '/Volumes/USB3-64/Image/4. 10164318 쁘띠프루티 카밍 앤 브라이트 페이셜 마스크팩.png'
    # filename = '/Volumes/USB3-64/Image/5. 10164572 참존 인텐시브 골드 앰플.jpg'
    # filename = '/Volumes/USB3-64/Image/6. 10166107 일동제약 퍼스트랩 프로바이오틱 마스크팩.png'
    # filename = '/Volumes/USB3-64/Image/6. 10166107 일동제약-1.png'
    # filename = '/Volumes/USB3-64/Image/6. 10166107 일동제약-2.png'
    # filename = '/Volumes/USB3-64/Image/6. 10166107 일동제약-3.png'
    # filename = '/Volumes/USB3-64/Image/7. 10167823 이오 에브리원 솝 코코넛레몬.jpg'
    filename = '/Volumes/USB3-64/Image/8. 10060298 티레이저 기기 + 크림.jpg'

    # filename = 'F:\\Image\\10167389_1.jpg'
    # filename = 'F:\\Image\\A1test.png'

    hndlr = OCRHandler()
    word_list = hndlr.detect_text(filename)

    # print('------------------------------------')
    count = 0
    for word  in word_list:
        print(word)
        # if count == 1592:
        #     print(word[0])
        #     print(word[1])
        #     pos_list = list(word[1])
        #     print(type(pos_list),  len(pos_list), pos_list)
        #     print(pos_list[0], pos_list[1], pos_list[2], pos_list[3])
        count = count + 1

