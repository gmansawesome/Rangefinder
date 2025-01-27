import os
import keyboard
import pyautogui
import pytesseract
import cv2
import numpy as np

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
    # readCoordinates()


def show_image(window_name, image):
    """Display an image in a window and wait for a key press."""
    cv2.imshow(window_name, image)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()


def readCoordinates():
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
    lower_white = np.array([0, 0, 180], dtype=np.uint8)  # Keep high brightness
    upper_white = np.array([255, 60, 255], dtype=np.uint8)  # Allow slight saturation

    # Create a mask that captures only white regions
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Apply the mask to keep only white text
    filtered = cv2.bitwise_and(resized, resized, mask=mask)
    show_image("Mask", filtered)

    # Convert to Grayscale
    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    show_image("Grayscale Image", gray)

    # Apply Binary Thresholding 
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    show_image("Thresholded Image", thresh)

    # Morphological Closing to Fill Gaps in Letters
    kernel = np.ones((3,3), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Morphological Dilation to Thicken Text Lines
    dilated = cv2.dilate(closed, kernel, iterations=6)
    show_image("Morphological Dilation", dilated)


    # OCR Configuration
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist="0123456789mAzimDst."'
    
    # Extract text
    extracted_text = pytesseract.image_to_string(dilated, config=custom_config)

    print(extracted_text)

    return extracted_text


def main():
    # keyboard.add_hotkey('p', captureScreenshot)

    # keyboard.wait('esc')

    readCoordinates()

# prevents main from running when imported as a library
if __name__ == "__main__":
    main()