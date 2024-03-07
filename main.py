import os
import pyautogui
import pytesseract
from PIL import Image
import cv2
import numpy as np

def captureScreenshot():
    # Get the current mouse cursor position
    cursor_x, cursor_y = pyautogui.position()

    # Calculate the region around the cursor to capture
    width = 45
    height = 35
    x1 = max(0, cursor_x-width)
    y1 = max(0, cursor_y+15)
    x2 = min(pyautogui.size()[0], cursor_x + width)
    y2 = min(pyautogui.size()[1], y1 + (height//2))

    # Capture the screen in the specified region
    distance = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    azumith = pyautogui.screenshot(region=(x1, y2, x2 - x1, y2 - y1))

    # Convert the screenshot to a NumPy array
    distanceNp = np.array(distance)
    azumithNp = np.array(azumith)

    # Set output folder
    output_folder = "numTemplates"
    os.makedirs(output_folder, exist_ok=True)

    # Save the screenshots as PNG files
    cv2.imwrite(os.path.join(output_folder, "distance.png"), distanceNp)
    cv2.imwrite(os.path.join(output_folder, "azumith.png"), azumithNp)

def readAzmDist():
    # Set path to tesseract OCR
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # distance_Img = Image.open('numTemplates\distance.png')
    # azumith_Img = Image.open('numTemplates\\azumith.png')

    # Open images and convert to grayscale
    distance_Img = cv2.imread('numTemplates\distance.png', cv2.IMREAD_GRAYSCALE)
    azumith_Img = cv2.imread('numTemplates\\azumith.png', cv2.IMREAD_GRAYSCALE)

    # Read strings from images
    distance = pytesseract.image_to_string(distance_Img)
    azumith = pytesseract.image_to_string(azumith_Img)

    print(distance)
    print(azumith)

    # Filter numerical values and convert to int
    distance = filterAzmDist(distance)
    azumith = filterAzmDist(azumith)

    return distance, azumith

def filterAzmDist(str):
    output = ''
    for c in str:
        if ord(c) >= 48 and ord(c) <= 57:
            output += c
    
    return int(output)

cv2.waitKey(4000)
captureScreenshot()

distance, azumith = readAzmDist()

print("Distance: ", distance)
print("Azumith: ", azumith)