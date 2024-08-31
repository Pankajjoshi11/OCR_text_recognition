import easyocr
import cv2
import numpy as np
import re
from spellchecker import SpellChecker

# Initialize the OCR reader for English
reader = easyocr.Reader(['en','hi'])

# Initialize the spell checker
spell = SpellChecker()

# Path to your image file
image_path = r'C:\Users\jorde\Desktop\SIH\img3.jpg'

# Load the image
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply GaussianBlur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply adaptive thresholding to enhance the text
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)

# Save the preprocessed image temporarily (if needed)
preprocessed_image_path = r'C:\Users\jorde\Desktop\SIH\preprocessed_img1.jpg'
cv2.imwrite(preprocessed_image_path, thresh)

# Read the text from the preprocessed image
results = reader.readtext(preprocessed_image_path)

# Function to sort bounding boxes: primarily by y-coordinate, then x-coordinate
def sort_by_position(boxes):
    return sorted(boxes, key=lambda box: (box[0][0][1], box[0][0][0]))

# Sort the OCR results
sorted_results = sort_by_position(results)

# Function to clean and correct spelling
def correct_spelling(text):
    # Clean up the text
    cleaned_text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Replace multiple spaces with single space

    # Correct spelling
    words = cleaned_text.split()
    corrected_words = [spell.correction(word) or word for word in words]  # Use original word if correction is None
    return ' '.join(corrected_words)

# Specify the path for the output text file
output_file_path = r'C:\Users\jorde\Desktop\SIH\output.txt'

# Open the file in write mode and write the sorted results into one line
with open(output_file_path, 'w', encoding='utf-8') as file:
    # Concatenate all sorted results into one line
    combined_text = ' '.join(result[1] for result in sorted_results)
    corrected_text = correct_spelling(combined_text)
    file.write(corrected_text + '\n')

print(f"OCR results with corrected spellings have been saved to {output_file_path}")
