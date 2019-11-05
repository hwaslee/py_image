import sys
import io
from google.cloud import vision
sys.path.insert(1, '/Users/andrew/Documents/py_basic/util')
import timeutil


def detect_text(path):
    ocrtimer = timeutil.TimeElapsed()
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Type(texts):', type(texts))
    # print('Texts:', texts)
    print('--------------------')

    print("\nOCR elapsed: ", ocrtimer.getelapsed())
    print('\nAll Data:')

    # ---- 전체 단어와 position을 나열한다
    count = 0
    for text in texts:
        newtext = text.description.replace('\n', ' ')
        print('{:>2} Desc:[{:>10s}],'.format(count, newtext), end='')

        vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices])
        # print('\n\tvertices:', vertices, ' Type:', type(vertices))
        print('bounds: {}'.format(','.join(vertices)))

        count = count + 1

    # ---- 해당하는 단어의 position을 가져온다
    print('--------------------')
    for text in texts:
        if text.description == '당도':
            for vertex in text.bounding_poly.vertices:
                print ('Found....', vertex)


if __name__ == '__main__':
    wholetimer = timeutil.TimeElapsed()
    detect_text('/Volumes/USB3-64/Image/10167389_1.jpg')
    print("\n\nTotal elapsed: ", wholetimer.getelapsed())