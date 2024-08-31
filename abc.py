import easyocr

def main():
    reader = easyocr.Reader(['en'])
    image_path = r'C:\Users\jorde\Desktop\SIH\image.jpg'
    result = reader.readtext(image_path)
    for detection in result:
        print(detection[1])

if __name__ == "__main__":
    main()
