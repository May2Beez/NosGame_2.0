import time

import cv2

import WindowCapture
import main_function
import vision
from static_data import *


def check_bat_over_bob(img, bat_pixel_rgb):
    if not detect_color(bat_pixel_rgb, img):
        return False
    else:
        return True


def solve_combo_fish(NosTale_window, data, human, hwnd):
    arrow_left, arrow_up, arrow_right, arrow_down = data

    combo = 0

    start = time.time()

    while combo < 8 and time.time() - start <= 4:
        try:
            img = NosTale_window.get_screenshot()
        except Exception:
            continue

        x = img.shape[1] / 2
        y = img.shape[0] / 2
        crop_img = img[int(y - 10):int(y + 25), int(x - 160):int(x + 230)].copy()

        if arrow_left.find(crop_img, threshold=0.95):
            main_function.click(hwnd, win32con.VK_LEFT, False, human, minigame="Combo_fish")
            combo += 1

        elif arrow_up.find(crop_img, threshold=0.95):
            main_function.click(hwnd, win32con.VK_UP, False, human, minigame="Combo_fish")
            combo += 1

        elif arrow_right.find(crop_img, threshold=0.95):
            main_function.click(hwnd, win32con.VK_RIGHT, False, human, minigame="Combo_fish")
            combo += 1

        elif arrow_down.find(crop_img, threshold=0.95):
            main_function.click(hwnd, win32con.VK_DOWN, False, human, minigame="Combo_fish")
            combo += 1

        time.sleep(0.1)

    time.sleep(0.2)


class Fishpond:
    bat_pixel_rgb = [(33, 36, 170), (32, 35, 170), (39, 49, 210)]
    catch_rgb = [(255, 247, 198), ]
    combo_fish_rgb = [(1, 218, 255), ]

    def __init__(self, hwnd):
        self.NosTale_hwnd = hwnd
        self.NosTale_window = WindowCapture.WindowCapture(window_hwnd=self.NosTale_hwnd)

    def find_bobs(self):
        left_bot_bob = vision.Vision(cv2.imread(resource_path("images/bob_left_bot.png")))
        right_top_bob = vision.Vision(cv2.imread(resource_path("images/bob_top_right.png")))

        if left_bot_bob and right_top_bob:
            time.sleep(0.1)
            img = self.NosTale_window.get_screenshot()
            left_bob, bot_bob = left_bot_bob.find(img, threshold=0.95)
            top_bob, right_bob = right_top_bob.find(img, threshold=0.95)

            if left_bob and bot_bob and top_bob and right_bob:
                return left_bob, bot_bob, top_bob, right_bob

    def get_scores(self):
        return [0, 1000, 4000, 8000, 12000, 20000]


class Sawmill:
    wood_rgb = [(20, 62, 88), (21, 59, 84), (22, 62, 88), (20, 61, 86)]

    def __init__(self, hwnd):
        self.NosTale_hwnd = hwnd
        self.NosTale_window = WindowCapture.WindowCapture(window_hwnd=self.NosTale_hwnd)

    def find_woods(self):

        chop_places = vision.Vision(cv2.imread(resource_path("images/chop_places.png")))

        while True:

            img = self.NosTale_window.get_screenshot()

            chop_top, chop_bot = chop_places.find(img, threshold=0.95)

            if chop_top and chop_bot:
                return chop_top, chop_bot

    def get_scores(self):
        return [0, 1010, 5010, 10010, 14010, 18010]
