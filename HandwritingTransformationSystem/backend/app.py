from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
from PIL import Image, ImageDraw, ImageFont
import textwrap
import pytesseract # type: ignore
import base64
from io import BytesIO
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route('/process', methods=['POST'])
def process_image():
    data = request.json
    
    # Get image data
    image_data = base64.b64decode(data['image'])
    image = Image.open(BytesIO(image_data))
    
    # Get text from image
    text = pytesseract.image_to_string(image)

    # Get options
    font_size = int(data['font_size'])
    text_color = data['text_color']
    page_color = data['page_color']
    page_width = int(data['page_width'])
    page_height = int(data['page_height'])
    handwriting_style = data['handwriting_style']
    
    # Create a blank image with the given background color
    image = Image.new("RGB", (page_width, page_height), page_color)
    draw = ImageDraw.Draw(image)

    # Map handwriting style to font file
    font_files = {
        "1": "1.ttf",
        "2": "2.ttf",
        "3": "3.ttf",
        "4": "4.ttf"
    }
    font_path = os.path.join("../fonts", font_files.get(handwriting_style, "1.ttf"))
    font = ImageFont.truetype(font_path, font_size)

    # Wrap text
    lines = textwrap.wrap(text, width=50)
    y_text = 15
    for line in lines:
        line_width, line_height = font.getbbox(line)[2:]
        draw.text(((page_width - line_width) / 2, y_text), line, font=font, fill=text_color)
        y_text += line_height

    # Save the image to a bytes buffer
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return jsonify({'processed_image': image_base64})

if __name__ == '__main__':
    app.run(debug=True)
