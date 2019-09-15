try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
### pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# Simple image to string
print("1. ", pytesseract.image_to_string(Image.open('subImage.png')))

# French text image to string
print("2. ", pytesseract.image_to_string(Image.open('subImage.png'), lang='kor'))

# Get bounding box estimates
print("3. ", pytesseract.image_to_boxes(Image.open('subImage.png')))

# Get verbose data including boxes, confidences, line and page numbers
print("4. ", pytesseract.image_to_data(Image.open('subImage.png')))

# Get information about orientation and script detection
print("5. ", pytesseract.image_to_osd(Image.open('subImage.png')))

# In order to bypass the internal image conversions, just use relative or absolute image path
# NOTE: If you don't use supported images, tesseract will return error
print("6. ",  pytesseract.image_to_string('subImage.png'))

# get a searchable PDF
pdf = pytesseract.image_to_pdf_or_hocr('subImage.png', extension='png')

# get HOCR output
### hocr = pytesseract.image_to_pdf_or_hocr('subImage', extension='hocr')