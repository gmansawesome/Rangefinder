import os
import pyautogui
import pytesseract
import cv2
import numpy as np
import re

def captureScreenshot():
    cursor_x, cursor_y = pyautogui.position()

    # Calculate the region around the cursor to capture
    width = 40
    height = 45
    x1 = max(0, cursor_x-width)
    y1 = max(0, cursor_y+10)
    x2 = min(pyautogui.size()[0], cursor_x+width)
    y2 = min(pyautogui.size()[1], y1+height)

    # Capture the screen in the specified region
    coordinates = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

    # Convert the screenshot to a NumPy array
    coordinatesNp = np.array(coordinates)

    # Set output folder
    output_folder = "numTemplates"
    os.makedirs(output_folder, exist_ok=True)

    # Save the screenshots as PNG files
    cv2.imwrite(os.path.join(output_folder, "coordinates.png"), coordinatesNp)

    # Run OCR
    return readScreenshot()


def show_image(window_name, image):
    # cv2.imshow(window_name, image)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()

def cleanScreenshotText(text):
    print(text)

    lines = text.strip().split("\n")

    if len(lines) < 2:
        print("Error: less than two lines found")
        return None, None
    
    dist_match = re.search(r'(\d+)', lines[0])
    azim_match = re.search(r'(\d+)', lines[1])

    if (dist_match == None or azim_match == None):
        print("Error: no numbers found")
        return None, None

    distance = int(dist_match.group(1))
    azimuth = int(azim_match.group(1))

    return distance, azimuth


def readScreenshot():
    # Set local path for tesseract-OCR
    pytesseract.pytesseract.tesseract_cmd = os.path.join(os.path.dirname(__file__), "tesseract-OCR", "tesseract.exe")
    
    # Load Image
    img = cv2.imread('numTemplates/coordinates.png')

    # Resize using cubic interpolation for better clarity
    scale_factor = 10
    resized = cv2.resize(img, (img.shape[1] * scale_factor, img.shape[0] * scale_factor), interpolation=cv2.INTER_CUBIC)
    show_image("Original Image", resized)

    # Convert to HSV (Hue, Saturation, Value) to detect bright whites
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

    # Define color range for white text (tuning required)
    lower_white = np.array([0, 0, 170], dtype=np.uint8)  # Keep high brightness
    upper_white = np.array([255, 40, 255], dtype=np.uint8)  # Allow slight saturation

    # Create a mask that captures only white regions
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Apply the mask to keep only white text
    filtered = cv2.bitwise_and(resized, resized, mask=mask)
    show_image("Mask", filtered)

    # Convert to Grayscale
    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    show_image("Grayscale Image", gray)

    # Apply Binary Thresholding 
    _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
    show_image("Thresholded Image", thresh)

    # Morphological Closing to Fill Gaps in Letters
    kernel = np.ones((3,3), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Morphological Dilation to Thicken Text Lines
    dilated = cv2.dilate(closed, kernel, iterations=4)
    show_image("Morphological Dilation", dilated)

    inverted = cv2.bitwise_not(dilated)
    show_image("Inverted", inverted)

    # OCR Configuration
    custom_config = r'--oem 3 --psm 6 -l eng -c tessedit_char_whitelist="0123456789mAzimDst."'
    
    # Extract text
    extracted_text = pytesseract.image_to_string(inverted, config=custom_config)

    return cleanScreenshotText(extracted_text)