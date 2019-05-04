# -*- coding: utf-8 -*-

from tkinter import Tk, Frame, Label, PhotoImage
from tkinter import messagebox
import threading
import logging

logger = logging.getLogger(__name__)
RED = "#ed2600"
LIGHT_RED = "#e84a4a"
YELLOW = "#febe2e"
DEFAULT_FONT = ("Arial", 14, "italic bold")
TAPIS = "#1D4231"


class GridScene:
    def __init__(self):
        self.columns_count = 0
        self.rows_count = 0
        self.lm = None

    def initialize_page(self, window_name, columns_count, rows_count, minus=0):
        global layout_manager
        self.lm = layout_manager
        self.lm.configure(bg=RED)
        self.lm.uno_frame.title("UNO - " + window_name)

        #   Remove old widgets
        for e in self.lm.grid_slaves():
            e.grid_forget()

        #   Cancel old columns/rows configuration
        for k in range(self.columns_count):
            self.lm.grid_columnconfigure(k, weight=0)
        for k in range(self.rows_count):
            self.lm.grid_rowconfigure(k, weight=0)

        #   Set new columns/rows values
        self.columns_count = columns_count
        self.rows_count = rows_count
        for k in range(self.columns_count-minus):
            self.lm.grid_columnconfigure(k, weight=1)
        for k in range(self.rows_count-minus):
            self.lm.grid_rowconfigure(k, weight=1)

    def load_image(self, path, divisor, background):
        image = PhotoImage(file=path)
        if divisor > 0:
            image = image.subsample(divisor)
        image_label = Label(self.lm, image=image, borderwidth=0, highlightthickness=0, bg=background)
        image_label.image = image
        return image_label

    def load_gif(self, path, background):
        gif = PhotoImage(file=path)
        gif_label = Label(self.lm, image=gif, borderwidth=0, highlightthickness=0, bg=background)

        def run_loop(gif_image):
            import time
            current_frame = 0
            max_frames = 0
            for i in range(999):
                try:
                    gif_image.configure(format="gif -index {}".format(str(i)))
                except:
                    max_frames = i
                    break

            while True:
                gif_image.configure(format="gif -index {}".format(str(current_frame)))
                current_frame = current_frame + 1 if (current_frame + 1) < max_frames else 0
                time.sleep(0.01)

        threading.Thread(target=run_loop, args=(gif,)).start()
        return gif_label


class LayoutManager(Frame):
    def __init__(self, frame):
        Frame.__init__(self, frame)
        self.uno_frame = frame
        self.grid(sticky="nsew")

        from graphics import HomeLayout, RulesLayout, PlayLayout, GameLayout, WaitingRoomLayout
        self.home = HomeLayout.HomeMenu()
        self.rules = RulesLayout.RulesMenu()
        self.play = PlayLayout.PlayMenu()
        self.game = GameLayout.GameMenu()
        self.waiting_room = WaitingRoomLayout.WaitingRoom()


def initialize_window():
    global layout_manager
    uno_frame = Tk()
    uno_frame.state('zoomed')
    uno_frame.minsize(900, 600)
    uno_frame.protocol("WM_DELETE_WINDOW", ask_quit)
    uno_frame.grid_propagate(False)
    uno_frame.grid_columnconfigure(0, weight=1)
    uno_frame.grid_rowconfigure(0, weight=1)

    layout_manager = LayoutManager(uno_frame)
    layout_manager.home.display()


def run_window():
    initialize_window()
    global layout_manager
    layout_manager.uno_frame.mainloop()


def ask_quit():
    def ask():
        if messagebox.askyesno("Quitter UNO", "Voulez-vous vraiment quitter? ⊙_⊙", icon=messagebox.WARNING):
            global layout_manager
            layout_manager.uno_frame.destroy()

    threading.Thread(target=ask, name="QuitThread").start()
