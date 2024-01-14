import pydirectinput
import time
import random
import pyautogui

from pynput.mouse import Controller
mouse = Controller()

def LamboRiderRun():
    GameOver = True
    try:
        if pyautogui.locateOnScreen('rc_items/gameimg.png', confidence=0.9) != None:
            print("Lambo Rider Miami clicked")
            image = pyautogui.locateOnScreen('rc_items/gameimg.png', confidence=0.9)
            if image != None:
                x, y = pyautogui.center(image)
                pyautogui.moveTo(x + 5, y + 20)
                time.sleep(2)
                pyautogui.click()
                GameOver = False
                time.sleep(5)
            
            if GameOver == False:
                print("locate Game Screen Area")
                if pyautogui.locateOnScreen('rc_items/GameArea.png', confidence=0.9) != None:
                    time.sleep(2)
                    GameArea = pyautogui.locateOnScreen('rc_items/GameArea.png', confidence=0.9)
                    print("Lambo Rider Game Area found")                    

                    try:
                        print("finding start button")
                        if pyautogui.locateOnScreen('rc_items/StartButton.png', confidence=0.9) != None:
                            image = pyautogui.locateOnScreen('rc_items/StartButton.png', confidence=0.9)
                            if image != None:
                                x, y = pyautogui.center(image)
                                pyautogui.moveTo(x, y)
                                time.sleep(1)
                                pyautogui.click()
                            
                                time.sleep(4)

                                pic = pyautogui.screenshot(region=(
                                int(GameArea.left), int(GameArea.top), int(GameArea.width),
                                int(GameArea.height)))
                                width, height = pic.size
                                offsetX = GameArea.left
                                offsetY = GameArea.top  + 10

                                while GameOver != True:
                                    print("Game running")

                                    mouse.position = (1337, 569)
                                    print("mouse moved to top ")
                                    r,g,b = pyautogui.pixel(1337,569)
                                    print(f"pixel color of top: R:{r}, G:{g}, B:{b}")
                                    time.sleep(2)
                                    
                                    mouse.position = (1337, 650)
                                    print("Mouse moved to middle row")
                                    r,g,b = pyautogui.pixel(1337,569)
                                    print(f"pixel color of midlle: R:{r}, G:{g}, B:{b}")
                                    time.sleep(2)

                                    mouse.position = (1337, 734)
                                    print("Mouse moved to bottom")
                                    r,g,b = pyautogui.pixel(1337,569)
                                    print(f"pixel color of bottom: R:{r}, G:{g}, B:{b}")
                                    time.sleep(2)




                    except Exception as e:
                        print(e)


    except Exception as e:
        print(e)



LamboRiderRun()