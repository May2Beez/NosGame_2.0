import threading

import main_function as Bot_function
from game_depends_function import *


class Bot(threading.Thread):
    def __init__(self, hwnd, minigame, repeats, level, human, gui, repeats_widget):
        super().__init__()
        self.gui = gui
        self.repeats_widget = repeats_widget
        self.NosTale_hwnd = hwnd
        self.minigame = minigame
        self.repeats = repeats
        self.level = level
        self.human = human
        self.searching = True
        self.NosTale_window = WindowCapture.WindowCapture(window_hwnd=self.NosTale_hwnd)

    def run(self):
        self.thread = threading.Thread(target=self.start_bot)
        self.thread.start()

    def start_bot(self):
        while self.searching:
            try:
                self.client = Bot_function.MainBot(self.minigame,
                                                   self.NosTale_hwnd,
                                                   self.NosTale_window,
                                                   self.level,
                                                   self.human,
                                                   self.repeats,
                                                   self.gui,
                                                   self.repeats_widget)
                self.client.setDaemon(True)
                self.client.if_start_exists(True)
                if self.minigame == "Fishpond":
                    fp = Fishpond(self.NosTale_hwnd)
                    data = fp.find_bobs()
                    score_levels = fp.get_scores()
                    self.client.set_score_levels(score_levels)
                    self.client.set_data(data)
                elif self.minigame == "Sawmill":
                    sm = Sawmill(self.NosTale_hwnd)
                    data = sm.find_woods()
                    score_levels = sm.get_scores()
                    self.client.set_score_levels(score_levels)
                    self.client.set_data(data)
                elif self.minigame == "Shooting":
                    pass
                elif self.minigame == "Quarry":
                    pass
                time.sleep(0.5)
                self.client.start()
                break
            except:
                continue

    def stop_bot(self):
        self.client.stop_bot()
        time.sleep(0.1)
