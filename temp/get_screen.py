from gymnasium import Env
from gymnasium.spaces import Box, Discrete
import numpy as np
import pyautogui
import pydirectinput
from PIL import Image

# Assuming the dimensions of the Box are left=749, top=538, width=394, height=315
left = 809
top = 646
width = 349
height = 278

# Calculate the right and bottom coordinates
right = left + width
bottom = top + height

# Now, you have the box dimensions in the format (left, top, right, bottom)
box_dimensions = (left, top, right, bottom)

# Capture the screen using pyautogui.screenshot
screenshot = pyautogui.screenshot()

# Crop the screenshot to the specified Box dimensions
cropped_screen = screenshot.crop(box_dimensions)

cropped_screen.show()
#cropped_screen.save("1.png")

print("Game screen captured")
