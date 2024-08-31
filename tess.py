import cv2
import pytesseract

# Uncomment and adjust this line if using Windows
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to the image containing handwritten text
image_path = 'img1.jpg'

# Read the image using OpenCV
image = cv2.imread(image_path)

# Check if the image was loaded correctly
if image is None:
    print("Error: Image not found or unable to read the image.")
else:
    print("Image loaded successfully.")

# Convert the image to grayscale (Tesseract works better with grayscale images)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Show the image to ensure it's loaded correctly (for debugging purposes)
cv2.imshow('Gray Image', gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Perform OCR on the image using Tesseract
detected_text = pytesseract.image_to_string(gray, lang='eng')

# Check if any text was detected
if not detected_text.strip():
    print("No text detected.")
else:
    # Print the detected text as a single line
    single_line_text = " ".join(detected_text.split())
    print(single_line_text)
