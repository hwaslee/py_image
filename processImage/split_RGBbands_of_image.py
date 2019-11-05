from PIL import Image


# Image.split() method is used to split the image into individual bands.
# This method returns a tuple of individual image bands (RGB bands) from an image.
# Splitting an “RGB” image creates three new images each containing a copy of one of the original bands (R,G,B).
# opening a multiband image (RGB specifically)
im = Image.open('/Volumes/USB3-64/Image/6. 10166107 일동제약 퍼스트랩 프로바이오틱 마스크팩.png')

# split() method
# this will split the image in individual bands
# and return a tuple
imgs = Image.Image.split(im)

print(len(imgs))

# showing each band
for img in imgs:
    img.show()