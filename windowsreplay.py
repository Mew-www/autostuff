import json
import time
import pyautogui
from windowskb import KEYMAP, type_key, hold_key, release_key

pyautogui.FAILSAFE = True


def replay_file(file_path, initial_delay=0):

    # Load steps from JSON config and optionally sleep
    steps = json.load(open(file_path, 'r'))
    time.sleep(initial_delay)

    # Keep track of timing and perform mouse/kb actions
    time_offset = steps[0][0]
    for step in steps:
        time.sleep(step[0] - time_offset)
        time_offset = step[0]

        if step[1].startswith('click'):
            pyautogui.click(x=int(step[2]), y=int(step[3]), duration=0.075, button=step[1][6:])

        if step[1].startswith('drag'):
            pyautogui.moveTo(x=int(step[2]), y=int(step[3]), duration=0.500)
            pyautogui.dragTo(x=int(step[5]), y=int(step[6]), duration=(step[4]-step[0]), button=step[1][5:])

        if step[1].startswith('type'):
            type_key(KEYMAP[step[1][5:]])

        if step[1].startswith('hold'):
            hold_key(KEYMAP[step[1][5:]])

        if step[1].startswith('release'):
            release_key(KEYMAP[step[1][8:]])
