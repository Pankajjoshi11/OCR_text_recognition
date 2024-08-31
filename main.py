from PIL import Image
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Load the image
image = Image.open('img1.jpg')

# Perform OCR to extract text
text = pytesseract.image_to_string(image)

# Print the extracted text (optional)
print("Extracted Text:")
print(text)

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

# Display the extracted information
print("\nExtracted Address Details:")
if names:
    print(f"Names: {names}")
else:
    print("No names found.")

if landmarks:
    print(f"Landmarks: {landmarks}")
else:
    print("No landmarks found.")

if pincodes:
    print(f"Pincodes: {pincodes}")
else:
    print("No pincodes found.")

if phone_numbers:
    print(f"Phone Numbers: {phone_numbers}")
else:
    print("No phone numbers found.")