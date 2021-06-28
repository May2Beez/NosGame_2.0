import random
import threading
import time
from tkinter import END

import cv2

import check_score
import static_data
import vision
from static_data import *
import win32api
import game_depends_function as games


def click(NosTale_hwnd, key, delay=True, human=False, minigame='Fishpond'):
    if human and minigame == "Fishpond":
        time.sleep(random.uniform(0.05, 0.22))
    win32gui.SendMessage(NosTale_hwnd, win32con.WM_KEYDOWN, key, 0x002C0001)
    win32gui.SendMessage(NosTale_hwnd, win32con.WM_KEYUP, key, 0xC02C0001)
    if delay:
        time.sleep(0.60)


class MainBot(threading.Thread):
    def __init__(self, minigame, NosTale_hwnd, NosTale_window, level, human, repeats, gui, repeats_widget):
        super().__init__()
        self.minigame = minigame
        self.repeats_widget = repeats_widget
        self.gui = gui
        self.NosTale_hwnd = NosTale_hwnd
        self.NosTale_window = NosTale_window
        self.repeats = repeats
        self.repeats_counter = 1
        self.level = level
        self.human = human
        self.RUNNING = False
        self.FAILED = False
        self.STOPPED = False

    def set_score_levels(self, score_levels):
        self.score_levels = score_levels

    def set_data(self, data):
        self.data = data

    def checking_score_thread(self):
        score_checker = check_score.CheckScore(
            cv2.imread(resource_path("images/score_digits.png"), cv2.IMREAD_GRAYSCALE))

        while self.RUNNING:

            try:

                img = self.NosTale_window.get_screenshot()

            except Exception:
                continue

            score_img_x = int(img.shape[1] / 2 - 181)
            score_img_y = int(img.shape[0] / 2 - 198)

            score_img = img[score_img_y:(score_img_y + 26), score_img_x:(score_img_x + 220)]

            score = score_checker.check_score(score_img)

            if score > int(self.score_levels[int(self.level)]):
                self.RUNNING = False
                self.FAILED = False
                break

            time.sleep(0.4)

    def if_start_exists(self, first=False, color='pale green'):
        start = time.time()
        while time.time() - start < 5:
            try:
                img = self.NosTale_window.get_screenshot()
            except:
                continue
            x, y = get_start_game_position(img)
            img = img[(y - 1):(y + 1), (x - 1):(x + 1)].copy()
            if detect_color(StaticData.start_game_rgb, img):
                lParam = win32api.MAKELONG(x, y)
                click_at(lParam, self.NosTale_hwnd)
                time.sleep(1)
                self.RUNNING = True
                self.FAILED = False
                if not first:
                    self.start_game(color)
                break
            time.sleep(1)

    def stop_bot(self):
        self.RUNNING = False
        self.STOPPED = True

    def run(self):
        self.thread = threading.Thread(target=self.start_game)
        self.thread.setDaemon(True)
        self.thread.start()

    def start_game(self, color='pale green'):
        self.gui.change_repeats(self.repeats_counter, self.repeats_widget, self.repeats, color)
        self.score = threading.Thread(target=self.checking_score_thread)
        combo_data = None
        if self.minigame == "Fishpond":
            arrow_left = vision.Vision(cv2.imread(resource_path("images/arrow_left.jpg")))
            arrow_up = vision.Vision(cv2.imread(resource_path("images/arrow_up.jpg")))
            arrow_right = vision.Vision(cv2.imread(resource_path("images/arrow_right.jpg")))
            arrow_down = vision.Vision(cv2.imread(resource_path("images/arrow_down.jpg")))
            combo_data = (arrow_left, arrow_up, arrow_right, arrow_down)
        elif self.minigame == "Sawmill":
            pass
        elif self.minigame == "Shooting":
            pass
        elif self.minigame == "Quarry":
            pass

        self.score.start()

        while self.RUNNING:

            if self.STOPPED:
                self.RUNNING = False
                break

            try:
                img = self.NosTale_window.get_screenshot()
            except Exception:
                continue

            if self.minigame == "Fishpond":
                left_bob_img = img[int(self.data[0][1] - 19):int(self.data[0][1] - 16),
                               int(self.data[0][0] + 8):int(self.data[0][0] + 14)].copy()
                bot_bob_img = img[int(self.data[1][1] - 19):int(self.data[1][1] - 16),
                              int(self.data[1][0] + 8):int(self.data[1][0] + 14)].copy()
                top_bob_img = img[int(self.data[2][1] - 19):int(self.data[2][1] - 16),
                              int(self.data[2][0] + 8):int(self.data[2][0] + 14)].copy()
                right_bob_img = img[int(self.data[3][1] - 19):int(self.data[3][1] - 16),
                                int(self.data[3][0] + 8):int(self.data[3][0] + 14)].copy()

                combo_fish_crop_img = img[int(self.data[0][1] - 16):int(self.data[0][1] - 13),
                                      int(self.data[0][0] - 30):int(self.data[0][0] - 25)].copy()

                if detect_color(games.Fishpond.combo_fish_rgb, combo_fish_crop_img):

                    games.solve_combo_fish(self.NosTale_window, combo_data, self.human, self.NosTale_hwnd)

                else:

                    if detect_color(games.Fishpond.catch_rgb, left_bob_img):
                        if not games.check_bat_over_bob(left_bob_img, games.Fishpond.bat_pixel_rgb):
                            click(self.NosTale_hwnd, win32con.VK_LEFT, True, self.human)

                    elif detect_color(games.Fishpond.catch_rgb, bot_bob_img):
                        if not games.check_bat_over_bob(bot_bob_img, games.Fishpond.bat_pixel_rgb):
                            click(self.NosTale_hwnd, win32con.VK_DOWN, True, self.human)

                    elif detect_color(games.Fishpond.catch_rgb, top_bob_img):
                        if not games.check_bat_over_bob(top_bob_img, games.Fishpond.bat_pixel_rgb):
                            click(self.NosTale_hwnd, win32con.VK_UP, True, self.human)

                    elif detect_color(games.Fishpond.catch_rgb, right_bob_img):
                        if not games.check_bat_over_bob(right_bob_img, games.Fishpond.bat_pixel_rgb):
                            click(self.NosTale_hwnd, win32con.VK_RIGHT, True, self.human)

                time.sleep(0.1)

            elif self.minigame == "Sawmill":
                chop_place_1_y = self.data[0][1] - 60
                chop_place_1_x = self.data[0][0] - 5
                chop_place_1 = img[int(chop_place_1_y):int(chop_place_1_y + 60),
                               int(chop_place_1_x):int(chop_place_1_x + 10)].copy()

                # Bottom chop place
                chop_place_2_y = self.data[1][1] - 60
                chop_place_2_x = self.data[1][0] - 5
                chop_place_2 = img[int(chop_place_2_y):int(chop_place_2_y + 60),
                               int(chop_place_2_x):int(chop_place_2_x + 10)].copy()

                if detect_color(games.Sawmill.wood_rgb, chop_place_1):

                    click(self.NosTale_hwnd, win32con.VK_LEFT, False, self.human, self.minigame)
                    time.sleep(0.3)

                elif detect_color(games.Sawmill.wood_rgb, chop_place_2):

                    click(self.NosTale_hwnd, win32con.VK_RIGHT, False, self.human, self.minigame)
                    time.sleep(0.3)

            # Full IMG
            try:
                fail_img = self.NosTale_window.get_screenshot()
            except Exception:
                continue

            # IMG for result window
            result_window_x = fail_img.shape[1] / 2 - 5
            result_window_y = fail_img.shape[0] / 2 - 60
            result_window_crop_img = fail_img[int(result_window_y):int(result_window_y + 10),
                                     int(result_window_x):int(result_window_x + 10)].copy()

            if detect_color(StaticData.result_window_rgb, result_window_crop_img):
                self.FAILED = True
                self.RUNNING = False
                break

        self.finished_game()

    def finished_game(self):
        self.score.join()

        if self.STOPPED:
            exit(0)

        else:

            if not self.FAILED:

                while True:

                    try:
                        img = self.NosTale_window.get_screenshot()
                    except Exception:
                        continue

                    # IMG for result window
                    result_window_x = img.shape[1] / 2 - 5
                    result_window_y = img.shape[0] / 2 - 60
                    result_window_crop_img = img[int(result_window_y):int(result_window_y + 10),
                                             int(result_window_x):int(result_window_x + 10)].copy()

                    if detect_color(StaticData.result_window_rgb, result_window_crop_img):
                        break

                    if self.minigame == "Fishpond":
                        click(self.NosTale_hwnd, win32con.VK_LEFT, False, False)

                    time.sleep(0.5)

                time.sleep(0.5)

                # Click Reward button
                while True:
                    try:
                        img = self.NosTale_window.get_screenshot()
                        break
                    except:
                        continue
                x, y = static_data.get_reward_position(img)
                lParam = win32api.MAKELONG(x, y)
                click_at(lParam, self.NosTale_hwnd)
                time.sleep(0.7)

                # Click level reward
                while True:
                    try:
                        img = self.NosTale_window.get_screenshot()
                        break
                    except:
                        continue
                x, y = static_data.get_level_reward_position(img, self.level)
                lParam = win32api.MAKELONG(x, y)
                click_at(lParam, self.NosTale_hwnd)
                time.sleep(0.7)

                while True:
                    try:
                        img = self.NosTale_window.get_screenshot()
                        break
                    except:
                        continue

                if self.repeats_counter < self.repeats:

                    chosen_options_x, chosen_options_y = static_data.get_play_again_position(img)

                else:

                    chosen_options_x, chosen_options_y = static_data.get_stop_position(img)
                    self.repeats_widget.configure(state='normal')
                    self.repeats_widget.configure(disabledbackground='cyan')
                    self.repeats_widget.delete(0, END)
                    self.repeats_widget.insert(0, str(self.repeats_counter) + "/" + str(self.repeats))
                    self.repeats_widget.configure(state='disabled')

                lParam = win32api.MAKELONG(chosen_options_x, chosen_options_y)
                click_at(lParam, self.NosTale_hwnd)
                time.sleep(0.7)

                while True:
                    try:
                        end_img = self.NosTale_window.get_screenshot()
                        break
                    except:
                        continue

                # IMG for result window
                result_window_x = end_img.shape[1] / 2 - 400 / 2
                result_window_y = end_img.shape[0] / 2 - 200 / 2
                result_window_crop_img = end_img[int(result_window_y):int(result_window_y + 200),
                                         int(result_window_x):int(result_window_x + 400)].copy()

                if vision.Vision(cv2.imread(resource_path("images/not_enough_points.png"))).find(result_window_crop_img,
                                                                                                 threshold=0.9):

                    self.repeats_widget.configure(state='normal')
                    self.repeats_widget.configure(disabledbackground='yellow')
                    self.repeats_widget.delete(0, END)
                    self.repeats_widget.insert(0, str(self.repeats_counter) + "/" + str(self.repeats))
                    self.repeats_widget.configure(state='disabled')

                    win32gui.SendMessage(self.NosTale_hwnd, win32con.WM_KEYDOWN, win32con.VK_ESCAPE, 0x002C0001)
                    win32gui.SendMessage(self.NosTale_hwnd, win32con.WM_KEYUP, win32con.VK_ESCAPE, 0xC02C0001)

                    chosen_options_x, chosen_options_y = static_data.get_stop_position(img)

                    lParam = win32api.MAKELONG(chosen_options_x, chosen_options_y)
                    click_at(lParam, self.NosTale_hwnd)
                    time.sleep(1)

                    coupon = vision.Vision(cv2.imread(resource_path("images/coupon_check.jpg")))

                    for i in range(4):
                        win32gui.SendMessage(self.NosTale_hwnd, win32con.WM_KEYDOWN, 0x30, 0x002C0001)
                        win32gui.SendMessage(self.NosTale_hwnd, win32con.WM_KEYUP, 0x30, 0xC02C0001)
                        time.sleep(0.2)
                        win32gui.SendMessage(self.NosTale_hwnd, win32con.WM_KEYDOWN, 0x30, 0x002C0001)
                        win32gui.SendMessage(self.NosTale_hwnd, win32con.WM_KEYUP, 0x30, 0xC02C0001)
                        time.sleep(0.2)

                        while True:
                            try:
                                coupon_img = self.NosTale_window.get_screenshot()
                                break
                            except:
                                continue

                        x_off = coupon_img.shape[1] / 2 - 150
                        y_off = coupon_img.shape[0] / 2 - 150

                        coupon_img = coupon_img[int(y_off):int(y_off+150), int(x_off):int(x_off+150)]

                        found = False

                        time_start = time.time()

                        while True and time.time() - time_start < 3:
                            if coupon.find(coupon_img, threshold=0.7):
                                found = True
                                break
                            time.sleep(0.2)

                        if found:
                            win32gui.SendMessage(self.NosTale_hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0x002C0001)
                            win32gui.SendMessage(self.NosTale_hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0xC02C0001)
                        else:
                            self.STOPPED = True
                            self.RUNNING = False
                            self.FAILED = False
                            break
                        time.sleep(0.6)

                    if self.STOPPED:
                        self.repeats_widget.configure(state='normal')
                        self.repeats_widget.configure(disabledbackground='LightPink1')
                        self.repeats_widget.configure(state='disabled')
                        exit(0)

                    while True:
                        try:
                            img = self.NosTale_window.get_screenshot()
                            break
                        except:
                            continue

                    open_game_x = img.shape[1] / 2 - 200 / 2
                    open_game_y = img.shape[0] / 2 - 200 / 2

                    img = img[int(open_game_y):int(open_game_y+200), int(open_game_x):int(open_game_x+200)]

                    open_game_location_x, open_game_location_y = vision.Vision(cv2.imread(resource_path("images/open_game.jpg"))).find(img, threshold=0.8)[0]

                    lParam = win32api.MAKELONG(int(open_game_x + open_game_location_x), int(open_game_y+open_game_location_y+5))
                    click_at(lParam, self.NosTale_hwnd)

                    time.sleep(0.5)

                    self.repeats_counter += 1

                    self.if_start_exists(first=True)
                    time.sleep(1)
                    self.if_start_exists(color='white')

                elif self.repeats_counter < self.repeats:

                    self.repeats_counter += 1
                    self.if_start_exists()

            else:
                time.sleep(0.1)

                while True:
                    try:
                        img = self.NosTale_window.get_screenshot()
                        break
                    except:
                        continue
                chosen_options_x, chosen_options_y = static_data.get_play_again_after_fail_position(img)

                lParam = win32api.MAKELONG(chosen_options_x, chosen_options_y)
                click_at(lParam, self.NosTale_hwnd)
                time.sleep(1)

                self.if_start_exists(color='salmon1')
