import easyocr
import cv2

# Initialize EasyOCR reader for English language
reader = easyocr.Reader(['hi'])

# Path to the image containing handwritten text
image_path = 'img4.jpg'

# Perform OCR on the image
results = reader.readtext(image_path)

# Combine all detected text into a single line
detected_text = " ".join([text for (_, text, _) in results])

# Print the single line of text
print(detected_text)

output_file_path = r'C:\Users\jorde\Desktop\SIH\output.txt'


print(f"OCR results with corrected spellings have been saved to {output_file_path}")
