import time
import os
import sys
import pyautogui
import json
import argparse

pyautogui.FAILSAFE = True

if __name__ == '__main__':

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--filename', dest='filename', default='history.txt')
    argparser.add_argument('--delay', dest='delay', default=0, type=int)
    args = argparser.parse_args()

    file_path = os.path.join(os.path.join(os.path.realpath(__file__)), '..', args.filename)
    steps = json.load(open(file_path, 'r'))
    time.sleep(args.delay)

    time_offset = steps[0][0]
    for step in steps:
        time.sleep(step[0] - time_offset)
        time_offset = step[0]

        if step[1].startswith('click'):
            pyautogui.click(x=int(step[2]), y=int(step[3]), duration=0.250, button=step[1][6:])

        if step[1].startswith('drag'):
            pyautogui.moveTo(x=int(step[2]), y=int(step[3]), duration=0.100)
            pyautogui.dragTo(x=int(step[5]), y=int(step[6]), duration=(step[4]-step[0]), button=step[1][5:])

        if step[1].startswith('type'):
            print('press', step[1][5:])
            pyautogui.press(step[1][5:])

        if step[1].startswith('hold'):
            print('hold', step[1][5:])
            pyautogui.keyDown(step[1][5:])

        if step[1].startswith('release'):
            print('release', step[1][8:])
            pyautogui.keyUp(step[1][8:])
c