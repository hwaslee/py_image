from PIL import Image
import os


def my_crop(im, path):
    # # im = Image.open(input)
    # # imgwidth, imgheight = im.size
    # for i in range(0, imgheight, src_height):
    #     for j in range(0, imgwidth, src_width):
    #         box = (j, i, j+src_width, i+src_height)
    #         a = im.crop(box)
    #         try:
    #             o = a.crop(area)
    #             o.save(os.path.join(path,"PNG","%s" % page,"IMG-%s.png" % k))
    #         except exception:
    #             pass
    #         k +=1
    # Here the image "im" is cropped and assigned to new variable im_crop
    box = (0, 0, im.width, im.height/3)
    im_crop = im.crop(box)
    im_crop.save(os.path.join('/Volumes/USB3-64/Image', "IMG-%s.png" % 1))
    box = (0, im.height/3, im.width, im.height*2/3)
    im_crop = im.crop(box)
    im_crop.save(os.path.join('/Volumes/USB3-64/Image', "IMG-%s.png" % 2))
    box = (0, im.height*2/3, im.width, im.height)
    im_crop = im.crop(box)
    im_crop.save(os.path.join('/Volumes/USB3-64/Image', "IMG-%s.png" % 3))


if __name__ == '__main__':
    im = Image.open('/Volumes/USB3-64/Image/6. 10166107 일동제약 퍼스트랩 프로바이오틱 마스크팩.png')
    imgwidth, imgheight = im.size
    my_crop(im, '/Volumes/USB3-64/Image')
    print('done...')