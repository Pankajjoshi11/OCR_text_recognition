import os
import spacy
import easyocr
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import re

# Set environment variable to avoid duplicate library warnings
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])

# Load spaCy model for NER
nlp = spacy.load('en_core_web_sm')

# Pre-process the image (if necessary)
def preprocess_image(image_path):
    try:
        # Open the image file
        image = Image.open(image_path)

        # Convert to grayscale
        image = image.convert('L')

        # Enhance the image sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(3)

        # Apply adaptive thresholding
        image = np.array(image)
        threshold = np.mean(image) * 0.8  # Lower the threshold for more aggressive binarization
        binary_image = (image > threshold) * 255
        image = Image.fromarray(binary_image.astype(np.uint8))

        # Enhance the image contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(3)

        # Apply a filter to reduce noise (optional)
        image = image.filter(ImageFilter.MedianFilter(3))

        # Apply Gaussian Blur to smooth out the image
        image = image.filter(ImageFilter.GaussianBlur(radius=1))

        # Resize the image
        width, height = image.size
        new_size = (width * 2, height * 2)
        image = image.resize(new_size, Image.LANCZOS)

        # Invert image colors if necessary
        image = ImageOps.invert(image)

        # Save the processed image
        processed_image_path = 'processed_' + os.path.basename(image_path)
        image.save(processed_image_path)

        return processed_image_path
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# Perform OCR to extract text
def extract_text_from_image(image_path):
    processed_image_path = preprocess_image(image_path)
    if processed_image_path:
        try:
            results = reader.readtext(processed_image_path, detail=0)
            return " ".join(results)
        except Exception as e:
            print(f"Error during OCR: {e}")
            return ""
    return ""

# Extract address details using spaCy NER and regex
def extract_address_details(text):
    doc = nlp(text)

    # Define improved patterns
    flat_pattern = r'\b(?:Flat\s\d+|Apt\s\d+|Suite\s\d+|Unit\s\d+|Room\s\d+|[0-9]+(?:[A-Za-z]+)?)\b'
    pincode_pattern = r'\b\d{5,6}\b'
    name_pattern = r'\b(?:Mr\.|Ms\.|Mrs\.|Dr\.)?\s?([A-Z]\.?\s?)+[A-Z][a-zA-Z]+\b'
    building_pattern = r'\b(?:\w+\s)?(?:Apartments|Building|Tower|Mansion|House|Complex|Block|Triveni)\s(?:\w+)?\b'
    city_pattern = r'\b(?:Delhi|Mumbai|Chennai|Kolkata|New York|London|Paris|Berlin|Sydney|Tokyo|NEW\sDELHI|BANGALORE|HYDERABAD|CHANDIGARH|PUNE|NOIDA|GURGAON)\b'

    # To exclude common titles
    exclude_titles = ['Mr', 'Ms', 'Mrs', 'Dr', 'Mr.', 'Ms.', 'Mrs.', 'Dr.']

    # Extracted fields
    name = ""
    building_name = ""
    flat_details = ""
    area = ""
    city = ""
    pincode = ""

    # Extract entities using spaCy
    for ent in doc.ents:
        if ent.label_ == "GPE":
            if not city:
                city = ent.text
            elif ent.text.lower() not in city.lower():
                area = ent.text  # Capture area only if it's different from city
        elif ent.label_ == "ORG":
            if not building_name:
                building_name = ent.text
        elif ent.label_ == "PERSON":
            if not name:
                name = ent.text

    # Extract flat details using regex
    flat_match = re.search(flat_pattern, text)
    flat_details = flat_match.group(0) if flat_match else "No flat details found."

    # Extract pincode using regex
    pincode_match = re.search(pincode_pattern, text)
    pincode = pincode_match.group(0) if pincode_match else "No pincodes found."

    # Extract name using regex if not found by spaCy
    if not name:
        name_match = re.search(name_pattern, text)
        name = name_match.group(0) if name_match else "No names found."

    # Extract building name using regex if not found by spaCy
    if not building_name:
        building_match = re.search(building_pattern, text)
        building_name = building_match.group(0) if building_match else "No building names found."

    # Extract city using regex if not found by spaCy
    if not city:
        city_match = re.search(city_pattern, text)
        city = city_match.group(0) if city_match else "No cities found."

    # Refine building name and area extraction if the extracted text contains both
    if building_name and ' ' in building_name:
        # Split into possible components
        parts = building_name.split(' ')
        if len(parts) > 1:
            building_name = ' '.join(parts[:-1])
            area = parts[-1] if area == "" else area  # If area not already set

    # Remove extra spaces and punctuation in areas and cities
    area = area.strip().replace(',', ' ')
    city = city.strip().replace(',', ' ')

    # Remove common titles from remaining text
    for title in exclude_titles:
        name = name.replace(title, '').strip()

    return {
        "Name": name,
        "Building Name": building_name,
        "Flat Details": flat_details,
        "Area": area if area else "No areas found.",
        "City": city if city else "No cities found.",
        "Pincode": pincode if pincode else "No pincodes found."
    }

# Set the path to your image file
image_path = 'img1.jpg'  # Replace with the actual path to your image

# Check if file exists
if not os.path.isfile(image_path):
    print("Image file not found.")
else:
    # Extract text from the image
    text = extract_text_from_image(image_path)

    # Extract address details using spaCy and regex
    address_details = extract_address_details(text)

    # Display the extracted information
    print("Extracted Text:")
    print(text)

    print("\nExtracted Address Details:")
    for key, value in address_details.items():
        print(f"{key}: {value}")