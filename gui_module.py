import time
import tkinter.font
from tkinter import *

import win32gui

import run_bot
from static_data import resource_path
from tkinter_custom_button import TkinterCustomButton

RUNNING = False
NOSTALE_WINDOWS = {}
CLIENTS_CANVAS = {}
BOTS = []


def center(toplevel, h, w):
    toplevel.update_idletasks()

    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()

    x = screen_width / 2 - w / 2
    y = screen_height / 2 - h / 2

    toplevel.geometry("%dx%d+%d+%d" % (w, h, x, y))


def rename_windows():
    global NOSTALE_WINDOWS

    NOSTALE_WINDOWS = {}

    def f(hwnd, more):
        title = win32gui.GetWindowText(hwnd)
        nostale_title = 'NosTale'
        if nostale_title in title:
            new_title = f"NosTale - ({hwnd})"
            NOSTALE_WINDOWS[hwnd] = new_title
            win32gui.SetWindowText(hwnd, new_title)

    win32gui.EnumWindows(f, None)


class Gui:
    def __init__(self):
        self.tk = Tk()
        self.tk.iconbitmap(resource_path("images/NosGame_icon.ico"))
        self.tk.title("NosGame by May2Bee")
        self.tk.resizable(False, False)
        center(self.tk, 400, 850)
        bot_title = Label(self.tk, text="NosGame - Minigames bot made by May2Bee", font=tkinter.font.Font(size=18))
        bot_title.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.clients_canvas()
        self.get_clients()
        self.put_buttons()
        self.tk.mainloop()

    def change_repeats(self, value, widget, counter, color):
        self.tk.nametowidget(str(widget)).configure(state='normal')
        self.tk.nametowidget(str(widget)).configure(disabledbackground=color)
        self.tk.nametowidget(str(widget)).delete(0, END)
        self.tk.nametowidget(str(widget)).insert(0, str(value) + "/" + str(counter))
        self.tk.nametowidget(str(widget)).configure(state='disabled')
        time.sleep(1)
        self.tk.nametowidget(str(widget)).configure(state='normal')
        self.tk.nametowidget(str(widget)).configure(disabledbackground='White')
        self.tk.nametowidget(str(widget)).configure(state='disabled')

    def get_clients(self):

        rename_windows()

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        gray = False

        index = 0

        global CLIENTS_CANVAS
        CLIENTS_CANVAS = {}

        for client in NOSTALE_WINDOWS:
            if gray:
                canvas = Canvas(self.scrollable_frame,
                                width=800,
                                height=30,
                                bg="gray82",
                                bd=0,
                                relief="ridge",
                                highlightthickness=0)
                gray = False
            else:
                canvas = Canvas(self.scrollable_frame,
                                width=800,
                                height=30,
                                bd=0,
                                relief="ridge",
                                highlightthickness=0)
                gray = True
            canvas.create_text((5, 15), text=NOSTALE_WINDOWS[client], font=tkinter.font.Font(size=11), anchor='w')

            minigame_value = StringVar(name="minigame" + str(index))
            minigame_value.set("Fishpond")
            minigames = ["Fishpond", "Sawmill"]
            minigames_menu = OptionMenu(canvas, minigame_value, *minigames)
            canvas.create_window(225, 15, window=minigames_menu)

            entry_repeats = Entry(canvas, width=12, font=tkinter.font.Font(size=11), justify=CENTER)
            entry_repeats.insert(END, "20")
            canvas.create_window(390, 15, window=entry_repeats)

            levels = [1, 2, 3, 4, 5]
            value_inside = IntVar(canvas, name="level" + str(index))
            value_inside.set(5)
            level_reward = OptionMenu(canvas, value_inside, *levels)
            canvas.create_window(540, 15, window=level_reward)

            is_human = BooleanVar(canvas, name="human" + str(index))
            check_mark_human = Checkbutton(canvas, variable=is_human, onvalue=True, offvalue=False)
            canvas.create_window(625, 15, window=check_mark_human)

            hold = BooleanVar(canvas, name="hold" + str(index))
            check_mark_hold = Checkbutton(canvas, variable=hold, onvalue=True, offvalue=False)
            canvas.create_window(695, 15, window=check_mark_hold)

            is_checked = BooleanVar(canvas, name="run" + str(index))
            check_mark = Checkbutton(canvas, variable=is_checked, onvalue=True, offvalue=False)
            canvas.create_window(765, 15, window=check_mark)

            canvas.pack()
            CLIENTS_CANVAS[client] = canvas
            index += 1

    def clients_canvas(self):
        font = tkinter.font.Font(size=12)
        label_info = [Label(self.tk, text="Client name", font=font),
                      Label(self.tk, text="Game", font=font),
                      Label(self.tk, text="Repeats Counter", font=font),
                      Label(self.tk, text="Level", font=font),
                      Label(self.tk, text="Human", font=font),
                      Label(self.tk, text="Hold", font=font),
                      Label(self.tk, text="Run?", font=font)]

        label_info[0].place(relx=0.12, rely=0.24, anchor=CENTER)
        label_info[1].place(relx=0.28, rely=0.24, anchor=CENTER)
        label_info[2].place(relx=0.48, rely=0.24, anchor=CENTER)
        label_info[3].place(relx=0.65, rely=0.24, anchor=CENTER)
        label_info[4].place(relx=0.75, rely=0.24, anchor=CENTER)
        label_info[5].place(relx=0.84, rely=0.24, anchor=CENTER)
        label_info[6].place(relx=0.92, rely=0.24, anchor=CENTER)

        container = Frame(self.tk, highlightbackground="black", highlightthickness=2)
        canvas = Canvas(container, width=800, height=200, bd=0, highlightthickness=0)
        scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container.place(relx=0.5, rely=0.55, anchor=CENTER)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def put_buttons(self):
        self.start_button = TkinterCustomButton(text="START",
                                                fg_color="green2",
                                                hover_color="green3",
                                                text_color='black',
                                                text_font=tkinter.font.Font(size=18, weight="bold"),
                                                width=200,
                                                corner_radius=10,
                                                command=self.start_bots)
        self.stop_button = TkinterCustomButton(text="STOP",
                                               fg_color="gray",
                                               hover_color="gray",
                                               hover=True,
                                               text_color='black',
                                               text_font=tkinter.font.Font(size=18, weight="bold"),
                                               width=200,
                                               corner_radius=10,
                                               command=self.stop_bots)
        self.refresh_button = TkinterCustomButton(text="REFRESH",
                                                  fg_color="cyan2",
                                                  hover_color="cyan3",
                                                  hover=True,
                                                  text_color='black',
                                                  text_font=tkinter.font.Font(size=18, weight="bold"),
                                                  width=200,
                                                  corner_radius=10,
                                                  command=self.refresh_bots)
        self.start_button.place(relx=0.2, rely=0.9, anchor=CENTER)
        self.stop_button.place(relx=0.8, rely=0.9, anchor=CENTER)
        self.refresh_button.place(relx=0.5, rely=0.9, anchor=CENTER)

    def start_bots(self):
        global RUNNING
        if not RUNNING:
            self.start_button.configure_color(fg_color="gray", hover_color="gray")
            self.stop_button.configure_color(fg_color="red2", hover_color="red3")
            self.refresh_button.configure_color(fg_color="gray", hover_color="gray")
            RUNNING = True
            index = 0
            for client in CLIENTS_CANVAS:
                if CLIENTS_CANVAS[client].winfo_exists():
                    repeats = level = human = minigame = repeats_widget = hold = 0
                    for widget in CLIENTS_CANVAS[client].winfo_children():
                        if "entry" in str(widget):
                            if widget.get():
                                if widget.get().isdigit():
                                    repeats = int(widget.get())
                                    repeats_widget = widget
                        elif "optionmenu" in str(widget) and "optionmenu2" not in str(widget):
                            minigame = widget.getvar(name="minigame" + str(index))
                        elif "optionmenu2" in str(widget):
                            level = widget.getvar(name="level" + str(index))
                        elif "checkbutton" in str(widget) and "checkbutton2" not in str(widget) and "checkbutton3" not in str(widget):
                            try:
                                human = widget.getvar(name="human" + str(index))
                            except:
                                pass
                        elif "checkbutton2" in str(widget):
                            try:
                                hold = widget.getvar(name="hold" + str(index))
                            except:
                                pass
                        elif "checkbutton3" in str(widget):
                            try:
                                if widget.getvar(name="run" + str(index)):
                                    bot = run_bot.Bot(client, minigame, repeats, level, human, self, repeats_widget, hold)
                                    bot.start()
                                    BOTS.append(bot)
                            except:
                                pass
                    index += 1
            for cli in CLIENTS_CANVAS:
                if CLIENTS_CANVAS[cli].winfo_exists():
                    for wid in CLIENTS_CANVAS[cli].winfo_children():
                        wid.configure(state="disabled")

    def stop_bots(self):
        global RUNNING
        if RUNNING:
            self.start_button.configure_color(fg_color="green2", hover_color="green3")
            self.stop_button.configure_color(fg_color="gray", hover_color="gray")
            self.refresh_button.configure_color(fg_color="cyan2", hover_color="cyan3")
            RUNNING = False
            for client in BOTS:
                client.stop_bot()
                client.join()
            for client in CLIENTS_CANVAS:
                if CLIENTS_CANVAS[client].winfo_exists():
                    for widget in CLIENTS_CANVAS[client].winfo_children():
                        widget.configure(state="normal")
                        if "entry" in str(widget):
                            widget.delete(0, END)
                            widget.insert(0, str(20))

    def refresh_bots(self):
        if not RUNNING:
            self.get_clients()
