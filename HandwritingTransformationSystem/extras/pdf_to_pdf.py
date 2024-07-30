from PIL import Image, ImageDraw, ImageFont
import textwrap
import pytesseract # type: ignore
import fitz  # PyMuPDF # type: ignore

# Path to the Tesseract executable 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to the PDF file containing handwritten text
pdf_path = 'hello.pdf'

# Function to convert PDF to images
def pdf_to_images(pdf_path):
    images = []
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

# Function to process images and perform OCR
def process_images(images):
    processed_images = []
    for image in images:
        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(image)
        
        # Initialize image parameters
        width, height = 480, 700
        background_color = "white"
        text_color = "black"
        
        # Create a blank image with white background
        new_image = Image.new("RGB", (width, height), background_color)
        draw = ImageDraw.Draw(new_image)
        
        # Load a handwriting-style font
        font_path = "1.ttf"  
        font_size = 20
        font = ImageFont.truetype(font_path, font_size)
        
        # Wrap text
        lines = textwrap.wrap(text, width=50)
        y_text = 15
        for line in lines:
            line_width, line_height = font.getbbox(line)[2:]
            draw.text(((width - line_width) / 2, y_text), line, font=font, fill=text_color)
            y_text += line_height
        
        processed_images.append(new_image)
    
    return processed_images

# Function to save images as a PDF
def save_images_as_pdf(images, output_path):
    images[0].save(output_path, save_all=True, append_images=images[1:])

# Convert PDF to images
input_images = pdf_to_images(pdf_path)

# Process images and perform OCR
processed_images = process_images(input_images)

# Save processed images as PDF
output_path = 'handwritten_text_output.pdf'
save_images_as_pdf(processed_images, output_path)
