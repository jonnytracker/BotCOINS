from gymnasium import Env
from gymnasium.spaces import Box, Discrete
import numpy as np

import pyautogui
import pydirectinput

from utils import get_screen, IMAGE_SIZE, reset_lives_ammount, start

window = None
try:
    if pyautogui.locateOnScreen('Start.png', confidence=0.7) is not None:
        
        window = pyautogui.locateOnScreen('Start.png', confidence=0.7)
except:
    try:
        if pyautogui.locateOnScreen('Restart.png', confidence=0.7) is not None:
            window = pyautogui.locateOnScreen('Restart.png', confidence=0.7)
    except:
        try: 
            if pyautogui.locateOnScreen('Restart2.png', confidence=0.7) is not None:
                window = pyautogui.locateOnScreen('Restart2.png', confidence=0.7)
        except:
            print("Game not found, program not started")
            exit()

print("Game window found")

r = get_screen(window)

print(window)