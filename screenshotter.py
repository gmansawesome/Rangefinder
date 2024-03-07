import os
import pyautogui
import pytesseract
import cv2
import numpy as np

def captureScreenshot():
    # Get the current mouse cursor position
    cursor_x, cursor_y = pyautogui.position()

    # Calculate the region around the cursor to capture
    width = 35
    height = 35
    x1 = max(0, cursor_x)
    y1 = max(0, cursor_y+15)
    x2 = min(pyautogui.size()[0], cursor_x + width)
    y2 = min(pyautogui.size()[1], y1 + (height//2))

    # Capture the screen in the specified region
    distance = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    azumith = pyautogui.screenshot(region=(x1, y2, x2 - x1, y2 - y1))

    # Convert the screenshot to a NumPy array
    distanceNp = np.array(distance)
    azumithNp = np.array(azumith)

    return distanceNp, azumithNp

cv2.waitKey(2000)
distance, azumith = captureScreenshot()

output_folder = "numTemplates"
os.makedirs(output_folder, exist_ok=True)

# Save the screenshots as PNG files
cv2.imwrite(os.path.join(output_folder, "distance.png"), distance)
cv2.imwrite(os.path.join(output_folder, "azumith.png"), azumith)

# Display the screenshot using OpenCV
# cv2.imshow("distance", distance)
# cv2.imshow("azumith", azumith)
# cv2.waitKey(10000)
# cv2.destroyAllWindows()

