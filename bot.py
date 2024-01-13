import pydirectinput
import time
import random

from utils import reset_lives_ammount, start, get_all_info, get_screen

# Mapping for action codes to pydirectinput-readable actions
ACTION_MAP = {
    1: 'up',
    2: 'down',
}

OcupiedLanes = [0, 0, 0]
CoinLanes = [0, 0, 0]
OCUPIEDLANETIME = 1.7

class LamboBot():
    def step(self):
        start_time = time.time()
        global OcupiedLanes
        global CoinLanes
        # Get the current game state information
        observation, _lives_lost, terminated =  get_all_info()

        for i in range(3):
            if observation["future_info"][i+3]: 
                OcupiedLanes[i] = OCUPIEDLANETIME
            if observation["coin"][i]:
                CoinLanes[i] = OCUPIEDLANETIME

        if observation["info"][observation["position"]+3]: # If there is something in front and im not moving away -> Move away randomly
            if observation["position"] == 1: # If im on toplane go down
                action = 2
            elif observation["position"] == 2: # If im on botlane go up
                action = 1 
            else: # Im on mid
                if OcupiedLanes[1] >= 0.2 or observation["info"][1]: # Im on mid and there is something on top
                    action = 2
                elif OcupiedLanes[2] >= 0.2 or observation["info"][2]: # Im on mid and there is something bottom
                    action = 1
                elif CoinLanes[1] != 0:
                    action = 1
                elif CoinLanes[2] != 0:
                    action = 2
                else: # else go to a random direction (There is nothing). Found out this works badly. Move down instead, it works more consistently
                    action = 2
                #action = 1
        else:
            action = 0

        # Works but its risky
        """if OcupiedLanes == [0, 0, 0]:
            if CoinLanes[0] != 0:
                if observation["position"] == 1:
                    action = 2
                elif observation["position"] == 2:
                    action = 1
            elif CoinLanes[1] != 0:
                action = 1
            elif CoinLanes[2] != 0:
                action = 2
            else:
                action = 0"""

        # Perform the action in the game using pydirectinput
        # 0 -> nothing, 1 -> up, 2 -> down
        if action != 0:
            pydirectinput.press(ACTION_MAP[action])

        elapsed = time.time() - start_time
        for i in range(3):
            OcupiedLanes[i] -= elapsed
            CoinLanes[i] -= elapsed
            if OcupiedLanes[i] < 0:
                OcupiedLanes[i] = 0
            if CoinLanes[i] < 0:
                CoinLanes[i] = 0
        return observation, terminated

    def reset(self):
        # Reset the number of lives and start the game
        reset_lives_ammount()
        global OcupiedLanes
        global CoinLanes
        OcupiedLanes = [0, 0, 0]
        CoinLanes = [0, 0, 0]
        start()

        # Obtain the initial game state
        observation = get_screen()
        return observation

# Create an instance of the LamboBot class
bot = LamboBot()

# Reset the game and continuously take steps until termination
obs = bot.reset()
while True:
    obs, terminated = bot.step()
    if terminated:
        bot.reset()


# OLD Alg
"""for i in range(3):
            if observation["info"][i+3]: 
                OcupiedLanes[i] = OCUPIEDLANETIME

        action = 0
        # All positions posible
        if observation["position"] == 1: # Top
            if OcupiedLanes[1] != 0: # Something top
                action = 2
        elif observation["position"] == 2: # Bot
            if OcupiedLanes[2] != 0: # Something bot
                action = 1
        elif observation["position"] == 0: # Mid
            if OcupiedLanes[0] != 0: # There is something close (to give time to see if a direction is better than the other (Get to less Dead-Ends))
                if OcupiedLanes[1] != 0:
                    action = 2
                else:
                    action = 1

        printable = [OcupiedLanes[1] != 0, OcupiedLanes[0] != 0, OcupiedLanes[2] != 0]
        print(printable)"""