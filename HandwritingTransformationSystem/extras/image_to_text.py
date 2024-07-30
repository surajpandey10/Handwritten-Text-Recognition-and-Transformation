import pytesseract # type: ignore
from PIL import Image

# Path to the Tesseract executable (change this if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to the image file containing handwritten text
image_path = 'Screenshot.png'

# Open the image file
image = Image.open(image_path)

# Use Tesseract to do OCR on the image
text = pytesseract.image_to_string(image)

# Print the recognized text
print("Recognized Text:")
print(text)
