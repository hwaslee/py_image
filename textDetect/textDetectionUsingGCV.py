# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/vision/cloud-client/detect/detect.py
# import argparse
import io
# import re
import sys
from datetime import datetime
from google.cloud import vision
# import sysutil
import pyperclip


# [START vision_text_detection]
def detect_text(file):
    tick = datetime.now()
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()
    sys.path.append('../util')
    # sys.path.append('..\\util')
    print(sys.path)

    # [START vision_python_migration_text_detection]
    with io.open(file, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    for text in texts:
        print("{}".format(text.description))
        # sysutil.copy2clip(text.description)
        pyperclip.copy(text.description)
        break;

    index  = 0
    for text in texts:
        # print('\n"{} {}"'.format(index, text.description))
        index += 1

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))

    tock = datetime.now()
    duration = tock - tick
    print("time elapsed: {:.2f} secs".format(duration.total_seconds()))
    # [END vision_python_migration_text_detection]
# [END vision_text_detection]


# [START vision_text_detection_gcs]
def detect_text_uri(uri):
    tick = datetime.now()
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    # sysutil.copy2clip(texts)
    sysutil.copy2clip(texts)

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    tock = datetime.now()
    duration = tock - tick
    print("time elapsed: {:.2f} secs".format(duration.total_seconds()))
# [END vision_text_detection_gcs]


if __name__ == '__main__':
    '''
    if len(sys.argv) < 2:
        print('Usage: python3 textDetectionUsingGCV.py <filename>')
        sys.exit(1)

    detect_text(sys.argv[1])
    '''

    # filename = '/Volumes/USB3-64/Image/transaction.PDF'
    filename = 'F:\\Image\\A1area.PNG'
    # filename = 'F:\\Image\\A1test.png'
    detect_text(filename)

