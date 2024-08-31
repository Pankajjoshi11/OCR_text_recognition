from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import re

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route('/extract', methods=['POST'])
def extract_info():
    # Get the image from the POST request
    image_file = request.files['image']
    image = Image.open(image_file)

    # Perform OCR to extract text
    text = pytesseract.image_to_string(image)

    # Regular expressions for extracting different components of the address
    name_pattern = r'([A-Za-z]+\s[A-Za-z]+)'  # Example pattern for name
    landmark_pattern = r'(Near\s[a-zA-Z\s]+|Opposite\s[a-zA-Z\s]+|Behind\s[a-zA-Z\s]+)'
    pincode_pattern = r'\b\d{6}\b'  # Pattern for 6-digit Indian pin code
    phone_number_pattern = r'\b\d{10}\b'  # Pattern for 10-digit phone number

    # Extracting information using regular expressions
    names = re.findall(name_pattern, text)
    landmarks = re.findall(landmark_pattern, text)
    pincodes = re.findall(pincode_pattern, text)
    phone_numbers = re.findall(phone_number_pattern, text)

    # Construct the response
    response = {
        'text': text,
        'names': names,
        'landmarks': landmarks,
        'pincodes': pincodes,
        'phone_numbers': phone_numbers
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
