# based a lot on https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# together with https://stackoverflow.com/questions/11906925/python-simulate-keydown
import ctypes
import time

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort
UINT = ctypes.c_uint


# https://docs.microsoft.com/en-us/windows/desktop/api/winuser/ns-winuser-taghardwareinput
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", DWORD),
                ("wParamL", ctypes.c_short),
                ("wParamH", WORD)]


# https://docs.microsoft.com/en-us/windows/desktop/api/winuser/ns-winuser-tagkeybdinput
class KeyboardInput(ctypes.Structure):
    _fields_ = [("wVk", WORD),
                ("wScan", WORD),
                ("dwFlags", DWORD),
                ("time", DWORD),
                ("dwExtraInfo", ULONG_PTR)]


# https://docs.microsoft.com/en-us/windows/desktop/api/winuser/ns-winuser-tagmouseinput
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", LONG),
                ("dy", LONG),
                ("mouseData", DWORD),
                ("dwFlags", DWORD),
                ("time", DWORD),
                ("dwExtraInfo", ULONG_PTR)]


# https://docs.microsoft.com/en-us/windows/desktop/api/winuser/ns-winuser-taginput
class InputUnion(ctypes.Union):
    _fields_ = [("ki", KeyboardInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


INPUT_MOUSE_TYPE = 0
INPUT_KEYBOARD_TYPE = 1
INPUT_HARDWARE_TYPE = 2


class Input(ctypes.Structure):
    _fields_ = [("type", DWORD),
                ("union", InputUnion)]


# https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-sendinput
def send_input(an_input):
    ctypes.windll.user32.SendInput(1, ctypes.pointer(an_input), ctypes.sizeof(an_input))


# https://docs.microsoft.com/en-us/windows/desktop/api/winuser/ns-winuser-tagkeybdinput
F_EXTENDEDKEY = 0x01  # For numpad keys
F_KEYUP = 0x02  # For release
F_SCANCODE = 0x08  # For using 2nd argument in determining key code (Scan Code, as opposed to Virtual Key Code)
F_UNICODE = 0x04  # For sending VK_PACKET emulating physical keyboard. For this wVk (1st argument) must be 0.


def hold_key(scan_code):
    kb_input = Input(INPUT_KEYBOARD_TYPE, InputUnion(ki=KeyboardInput(0, scan_code, F_SCANCODE, 0, None)))
    send_input(kb_input)


def release_key(scan_code):
    # https://docs.microsoft.com/en-us/windows/desktop/api/winuser/ns-winuser-tagkeybdinput
    kb_input = Input(INPUT_KEYBOARD_TYPE, InputUnion(ki=KeyboardInput(0, scan_code, F_SCANCODE | F_KEYUP, 0, None)))
    send_input(kb_input)


def type_key(scan_code):
    hold_key(scan_code)
    time.sleep(0.2)
    release_key(scan_code)


KEYMAP = {
    'ESCAPE': 0x01,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0A,
    '0': 0x0B,
    'MINUS': 0x0C,
    'EQUALS': 0x0D,
    'BACK': 0x0E,
    'TAB': 0x0F,
    'Q': 0x10,
    'W': 0x11,
    'E': 0x12,
    'R': 0x13,
    'T': 0x14,
    'Y': 0x15,
    'U': 0x16,
    'I': 0x17,
    'O': 0x18,
    'P': 0x19,
    'LBRACKET': 0x1A,
    'RBRACKET': 0x1B,
    'RETURN': 0x1C,
    'LCONTROL': 0x1D,
    'A': 0x1E,
    'S': 0x1F,
    'D': 0x20,
    'F': 0x21,
    'G': 0x22,
    'H': 0x23,
    'J': 0x24,
    'K': 0x25,
    'L': 0x26,
    'SEMICOLON': 0x27,
    'APOSTROPHE': 0x28,
    'GRAVE': 0x29,
    'LSHIFT': 0x2A,
    'BACKSLASH': 0x2B,
    'Z': 0x2C,
    'X': 0x2D,
    'C': 0x2E,
    'V': 0x2F,
    'B': 0x30,
    'N': 0x31,
    'M': 0x32,
    'COMMA': 0x33,
    'PERIOD': 0x34,
    'SLASH': 0x35,
    'RSHIFT': 0x36,
    'MULTIPLY': 0x37,
    'LMENU': 0x38,
    'SPACE': 0x39,
    'CAPITAL': 0x3A,
    'F1': 0x3B,
    'F2': 0x3C,
    'F3': 0x3D,
    'F4': 0x3E,
    'F5': 0x3F,
    'F6': 0x40,
    'F7': 0x41,
    'F8': 0x42,
    'F9': 0x43,
    'F10': 0x44,
    'NUMLOCK': 0x45,
    'SCROLL': 0x46,
    'NUMPAD7': 0x47,
    'NUMPAD8': 0x48,
    'NUMPAD9': 0x49,
    'SUBTRACT': 0x4A,
    'NUMPAD4': 0x4B,
    'NUMPAD5': 0x4C,
    'NUMPAD6': 0x4D,
    'ADD': 0x4E,
    'NUMPAD1': 0x4F,
    'NUMPAD2': 0x50,
    'NUMPAD3': 0x51,
    'NUMPAD0': 0x52,
    'DECIMAL': 0x53,
    'F11': 0x57,
    'F12': 0x58,
    'F13': 0x64,
    'F14': 0x65,
    'F15': 0x66,
    'KANA': 0x70,
    'CONVERT': 0x79,
    'NOCONVERT': 0x7B,
    'YEN': 0x7D,
    'NUMPADEQUALS': 0x8D,
    'CIRCUMFLEX': 0x90,
    'AT': 0x91,
    'COLON': 0x92,
    'UNDERLINE': 0x93,
    'KANJI': 0x94,
    'STOP': 0x95,
    'AX': 0x96,
    'UNLABELED': 0x97,
    'NUMPADENTER': 0x9C,
    'RCONTROL': 0x9D,
    'NUMPADCOMMA': 0xB3,
    'DIVIDE': 0xB5,
    'SYSRQ': 0xB7,
    'RMENU': 0xB8,
    'HOME': 0xC7,
    'UP': 0xC8,
    'PRIOR': 0xC9,
    'LEFT': 0xCB,
    'RIGHT': 0xCD,
    'END': 0xCF,
    'DOWN': 0xD0,
    'NEXT': 0xD1,
    'INSERT': 0xD2,
    'DELETE': 0xD3,
    'LWIN': 0xDB,
    'RWIN': 0xDC,
    'APPS': 0xDD
}
