import time
import os
import sys
import pyHook
import pythoncom
import json

#  keyboard_down[event.Key] = time.time()
#  print('MessageName:', event.MessageName)
#  print('Message:', event.Message)
#  print('Time:', event.Time)
#  print('Window:', event.Window)
#  print('WindowName:', event.WindowName)
#  print('Ascii:', event.Ascii, chr(event.Ascii))
#  print('Key:', event.Key)
#  print('---')


if __name__ == '__main__':

    configfile_path = os.path.join(os.path.join(os.path.realpath(__file__)), '..', 'history.txt')
    hm = pyHook.HookManager()
    steps = []  # Configuration to save
    mouse_down = {}  # {'Button': {time: time_pressed, x: x, y: y}, ...}
    keyboard_down = {}  # {'Key': time_pressed, ...}

    def on_mouse_down_and_up(button_name):

        def on_mouse_down(event):
            x, y = event.Position
            mouse_down[button_name] = {'time': time.time(), 'x': str(x), 'y': str(y)}
            return True

        def on_mouse_up(event):
            press = mouse_down[button_name]
            if (time.time() - press['time']) < 0.150:
                steps.append([press['time'], 'click_{}'.format(button_name), press['x'], press['y']])
            else:
                x, y = event.Position
                steps.append([press['time'], 'drag_{}'.format(button_name), press['x'], press['y'], time.time(), x, y])
            return True

        return on_mouse_down, on_mouse_up

    def on_keyboard_down_event(event):
        if event.KeyID == 164:  # Left ALT
            with open(configfile_path, 'w') as fh:
                json.dump(sorted(steps, key=lambda e: e[0]), fh)
            hm.UnhookMouse()
            hm.UnhookKeyboard()
            sys.exit(0)
        event_key = event.Key.upper()
        if event_key in keyboard_down:
            return True  # Pressing down key
        keyboard_down[event_key] = time.time()
        return True

    def on_keyboard_up_event(event):
        event_key = event.Key.upper()
        if event_key not in keyboard_down:
            return True  # May occur during an initial [ENTER] or so
        press_time = keyboard_down[event_key]
        # if (time.time() - press_time) < 0.2:
        #     steps.append([press_time, 'type_{}'.format(event_key)])
        # else:
        steps.append([press_time, 'hold_{}'.format(event_key)])
        steps.append([time.time(), 'release_{}'.format(event_key)])
        del keyboard_down[event_key]
        return True

    mouse_left_down, mouse_left_up = on_mouse_down_and_up('left')
    mouse_right_down, mouse_right_up = on_mouse_down_and_up('right')
    hm.SubscribeMouseLeftDown(mouse_left_down)
    hm.SubscribeMouseLeftUp(mouse_left_up)
    hm.SubscribeMouseRightDown(mouse_right_down)
    hm.SubscribeMouseRightUp(mouse_right_up)
    hm.HookMouse()

    hm.KeyDown = on_keyboard_down_event
    hm.KeyUp = on_keyboard_up_event
    hm.HookKeyboard()

    try:
        pythoncom.PumpMessages()
    except KeyboardInterrupt:
        pass
