import pyautogui
import dxcam
import numpy as np

import time

IMAGE_SIZE = 80


# Global variable to store the location of the lives indicator
lives_location = None
def get_lives_location():
    global lives_location
    if lives_location != None:
        return lives_location
    else:
        try:
            # Attempt to locate the 'Lives' indicator on the screen
            lives_location = pyautogui.locateOnScreen('images/Lives.png', confidence=0.9)
            return lives_location
        except:
            return None
        
def reset_lives_location():
    # Reset the lives location to None
    global lives_location
    lives_location = None

# Global variable to store the game window location
window = None
def locate_screen():
    global window
    if window == None:
        try:
            # Attempt to locate the 'Start' button on the screen
            if pyautogui.locateOnScreen('images/Start.png', confidence=0.7) is not None:
                
                window = pyautogui.locateOnScreen('images/Start.png', confidence=0.7)
                print("Game window found")
        except:
            print("Game not found, program not started")
            exit()
    
def start():
    # Function to start the game
    time.sleep(0.5)
    try:
        if pyautogui.locateOnScreen('images/StartButton.png', confidence=0.8) is not None:
            print("Game button found")
            image = pyautogui.locateOnScreen('images/StartButton.png', confidence=0.8)
            if image is not None:
                x, y = pyautogui.center(image)
                pyautogui.moveTo(x + 5, y+20)
                time.sleep(0.1)
                pyautogui.click()
                locate_screen()
                time.sleep(4)
    except:
        try: 
            if pyautogui.locateOnScreen('images/RestartButton.png', confidence=0.8) is not None:
                image = pyautogui.locateOnScreen('images/RestartButton.png', confidence=0.8)
                if image is not None:
                    x, y = pyautogui.center(image)
                    pyautogui.moveTo(x + 5, y + 20)
                    time.sleep(0.1)
                    pyautogui.click()
                    locate_screen()
                    time.sleep(4.1)
        except:
            print("Start button not found, the game window might have moved")
            print("Try to click it manualy or cancel the execution")

# Function to check if one array is present inside another array
def is_array_inside(arr, sub_arr):
    return any(np.array_equal(row, sub_arr) for row in arr)

# Function to get the color of a pixel in a given location on the screen
def get_pixel_color(screen, location, pixel_x, pixel_y):
    # Calculate the absolute coordinates of the pixel within the screen
    absolute_x = location.left + pixel_x
    absolute_y = location.top + pixel_y

    pixel_color = screen[absolute_y][absolute_x]

    return np.ndarray.tolist(pixel_color)

# Create a camera object for video capture
camera = dxcam.create()
camera.start()
# Initialize variables related to the game state


lives_ammount = 3
key_locations_x = [1337, 1337, 1337]
future_key_locations_x = [565, 565, 565]
key_locations_y = [553, 635, 718]
car_color = np.array([[255, 213,  65], [255, 213, 65], [255, 213, 65]], dtype=np.uint8)
floor_color = np.array([153, 138, 141], dtype=np.uint8)
floor_colors = np.array([[153, 138, 141], [141, 127, 131], [132, 137, 154], [128, 132, 149], [179, 185, 209], [123, 127, 143], [193, 199, 215], [153, 172, 181], [180, 32, 42], [155, 148, 140], [186, 186, 179], [147, 132, 136], [128, 133, 150], [196, 202, 217], [74, 66, 68], [144, 130, 134], [177, 183, 207], [218, 224, 234]], dtype=np.uint8)
prev_position = 0
coin_y_positions = [797, 670, 924]

# Function to gather information about the game state
def get_all_info():
    global window
    frame = camera.get_latest_frame()

    key_pixels = []
    future_key_pixels = []
    coin_pixels = []
    # Collect pixel information for key positions and coin positions
    for i in range(6): # 6 Key positions
        key_pixels.append(frame[key_locations_y[i], key_locations_x[i]])
        future_key_pixels.append(frame[key_locations_y[i], future_key_locations_x[i]])
        if i >= 3:
            coin_pixels.append(frame[coin_y_positions[i-3], key_locations_x[i]])

    position = None
    for i in range(3): # The first 3 positions are where the car can be
        if np.array_equal(key_pixels[i], car_color[i]):
            position = i
            break

    global prev_position
    if position == None:
        position = prev_position
    else:
        prev_position = position

    ocup = [False, False, False, False, False, False]
    coin = [False, False, False]
    for i in range(6):
        if not is_array_inside(floor_colors, key_pixels[i]): # If not floor, check if car
            if i != position: # If not floor, nor car
                if i >= 3:
                    if not np.array_equal(coin_pixels[i-3], floor_color): # If the coin gap doesnt exist (there is no coin)
                        if i-3 == position:
                            print(f"Block on: {i-3}. Im on: {position}. Pixel Color: {key_pixels[i]}")
                        ocup[i] = True
                    else:
                        coin[i-3] = True
                else:
                    ocup[i] = True

    # Futures
    future_ocup = [False, False, False, False, False, False]
    for i in range(6):
        if not is_array_inside(floor_colors, future_key_pixels[i]): # If not floor, check if car
            if i != position: # If not floor, nor car
                if i >= 3:
                    if not np.array_equal(coin_pixels[i-3], floor_color): # If the coin gap doesnt exist (there is no coin)
                        future_ocup[i] = True
                else:
                    future_ocup[i] = True

    obs = {
            "position": position,
            "info": np.array(ocup),
            "future_info": np.array(future_ocup),
            "coin": np.array(coin)
        }
    
    global lives_ammount
    live_lost = False
    terminated = False
    try:
        if lives_ammount == 3:
            pixel = get_pixel_color(frame, get_lives_location(), 631, 137)
            if pixel != [173, 90, 81]:
                print("2 lives left")
                lives_ammount = 2
                live_lost = True

        elif lives_ammount == 2:
            pixel = get_pixel_color(frame, get_lives_location(), 613, 137)
            if pixel != [173, 90, 81]:
                print("1 lives left")
                lives_ammount = 1
                live_lost = True
            
        if lives_ammount == 1:
            pixel = get_pixel_color(frame, get_lives_location(), 597, 137)
            if pixel != [173, 90, 81]:
                print("0 lives left, restarting")
                lives_ammount = 0
                live_lost = True
                terminated = True
    except:
        pass

    return (obs, live_lost, terminated)

# Function to reset the number of lives to the default value
def reset_lives_ammount():
    global lives_ammount
    lives_ammount = 3

# Cooldown period for updating the car position
cooldown_period = 1.0
last_update_time = time.time()

# Function to update the car position based on the action taken
def update_position(action):
    global prev_position, last_update_time

    current_time = time.time()

    if current_time - last_update_time >= cooldown_period:
        if action != 0:
            if action == 1: # Going up
                if prev_position == 0: # On mid
                    prev_position = 1
                elif prev_position == 1: # On top
                    pass
                else: # On bot
                    prev_position = 0
            elif action == 2: # Going down
                if prev_position == 0: # On mid
                    prev_position = 2
                elif prev_position == 1: # On top
                    prev_position = 0
                else: # On bot
                    pass
        last_update_time = current_time

def get_screen():
    global window
    frame = camera.get_latest_frame()

    key_pixels = []
    for i in range(6): # 6 Key positions
        key_pixels.append(frame[key_locations_y[i], key_locations_x[i]])

    position = None
    for i in range(3): # The first 3 positions are where the car can be
        if np.array_equal(key_pixels[i], car_color[i]):
            position = i
            break

    global prev_position
    if position == None:
        position = prev_position
    else:
        prev_position = position

    ocup = [False, False, False, False, False, False]
    for i in range(6):
        if not np.array_equal(key_pixels[i], floor_color): # If not floor, check if car
            if i != position: # If not floor, nor car
                ocup[i] = True

    return {
            "position": position,
            "info": np.array(ocup)
        }

