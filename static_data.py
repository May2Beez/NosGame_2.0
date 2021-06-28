import os
import sys

import numpy as np
import win32con
import win32gui
from PIL import Image


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_resolution(window):
    resolutions = [(1024, 768), (1280, 1024), (1280, 800), (1440, 900), (1024, 700), (1680, 1050)]
    img = window.get_screenshot()
    y, x, _ = img.shape

    if (x, y) in resolutions:
        return resolutions.index((x, y))
    else:
        return -1


# Check if RGB value is on image (for checking if Bat is over bob)
def detect_color(rgb, img):
    pix = Image.fromarray(np.uint8(img)).convert('RGB')

    pix = pix.load()

    for y in range(0, img.shape[0]):
        for x in range(0, img.shape[1]):
            if pix[x, y] in rgb:
                return True
    return False


def get_start_game_position(img):
    return int(img.shape[1] / 2), int(img.shape[0] / 2 + 160)


def get_reward_position(img):
    return int(img.shape[1] / 2 + 130), int(img.shape[0] / 2 + 50)


def get_level_reward_position(img, level):
    level = int(level)
    diff = [-2, -1, 0, 1, 2]
    x_diff = 70 * diff[level-1]
    return int(img.shape[1] / 2 + x_diff), int(img.shape[0] / 2 + 55)


def get_stop_position(img):
    return int(img.shape[1] / 2 + 40), int(img.shape[0] / 2 + 80)


def get_play_again_position(img):
    return int(img.shape[1] / 2 - 40), int(img.shape[0] / 2 + 80)


def get_play_again_after_fail_position(img):
    return int(img.shape[1] / 2 - 130), int(img.shape[0] / 2 + 60)


def click_at(lParam, hwnd):
    win32gui.SendMessage(hwnd, win32con.WM_MOUSEMOVE, None, lParam)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)


class StaticData:
    result_window_rgb = [(247, 168, 150), ]
    start_game_rgb = [(190, 117, 52), ]
