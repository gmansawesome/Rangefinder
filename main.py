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
    width = 35
    height = 32
    x1 = max(0, cursor_x-width)
    y1 = max(0, cursor_y+15)
    x2 = min(pyautogui.size()[0], cursor_x + width)
    y2 = min(pyautogui.size()[1], y1 + (height//2))

    # Capture the screen in the specified region
    distance = pyautogui.screenshot(region=(x1, y1+1, x2 - x1, y2 - y1))
    azumith = pyautogui.screenshot(region=(x1, y2+3, x2 - x1, y2 - y1))

    # Convert the screenshot to a NumPy array
    distanceNp = np.array(distance)
    azumithNp = np.array(azumith)

    # Set output folder
    output_folder = "numTemplates"
    os.makedirs(output_folder, exist_ok=True)

    # Save the screenshots as PNG files
    cv2.imwrite(os.path.join(output_folder, "distance.png"), distanceNp)
    cv2.imwrite(os.path.join(output_folder, "azumith.png"), azumithNp)

def readAzimDist():
    # Set path to tesseract OCR
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Open images
    distance_Img = cv2.imread('numTemplates\distance.png')
    azumith_Img = cv2.imread('numTemplates\\azumith.png')

    distance_PP = cv2.cvtColor(distance_Img, cv2.COLOR_BGR2GRAY)
    azumith_PP = cv2.cvtColor(azumith_Img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    # distance_PP = cv2.GaussianBlur(distance_PP, (2, 2), 0)
    # azumith_PP = cv2.GaussianBlur(azumith_PP, (3, 3), 0)

    # fitler with threshold
    _, distance_PP = cv2.threshold(distance_PP, 150, 255, cv2.THRESH_BINARY)
    _, azumith_PP = cv2.threshold(azumith_PP, 150, 255, cv2.THRESH_BINARY)

    # Resize the image to fit the screen
    screen_width = int(1920)   
    screen_height = int(1920 * (distance_Img.shape[0]/distance_Img.shape[1]))   

    # # Show distance
    # distance_Res = cv2.resize(distance_Img, (screen_width, screen_height), interpolation=cv2.INTER_CUBIC)
    # cv2.imshow("", distance_Res)
    # cv2.waitKey(2000)
    # distance_Res = cv2.resize(distance_PP, (screen_width, screen_height), interpolation=cv2.INTER_CUBIC)
    # cv2.imshow("", distance_Res)
    # cv2.waitKey(2000)
    # # Show azumith
    # azumith_Res = cv2.resize(azumith_Img, (screen_width, screen_height), interpolation=cv2.INTER_CUBIC)
    # cv2.imshow("", azumith_Res)
    # cv2.waitKey(2000)
    # azumith_Res = cv2.resize(azumith_PP, (screen_width, screen_height), interpolation=cv2.INTER_CUBIC)
    # cv2.imshow("", azumith_Res)
    # cv2.waitKey(2000)

    # Read strings from images
    distance = pytesseract.image_to_string(distance_PP)
    azumith = pytesseract.image_to_string(azumith_PP)

    # Filter out everything but numerical values
    distance_filtered = filterAzimDist(distance)
    azumith_filtered = filterAzimDist(azumith)

    print(distance, "->", distance_filtered)
    print(azumith, "->", azumith_filtered)

    return distance_filtered, azumith_filtered

def filterAzimDist(str):
    output = ''
    for c in str:
        if ord(c) >= 48 and ord(c) <= 57:
            output += c
    
    return output

cv2.waitKey(4000)
captureScreenshot()

distance, azumith = readAzimDist()

# print("Distance:", distance)
# print("Azumith:", azumith)