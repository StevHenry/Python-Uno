from graphics.window import *
from tkinter import Label, Button


class HomeMenu(GridScene):
    def __init__(self):
        GridScene.__init__(self)

    def display(self):
        self.initialize_page("Menu principal", 3, 6, minus=1)
        #   Logo:
        self.load_image("resources/pictures/Logo (2).png", 1, RED).grid(row=0, column=0, columnspan=self.columns_count)
        #   Play:
        Button(self.lm, text="JOUER", activebackground=YELLOW, bg=YELLOW, fg=RED, activeforeground=RED, relief='solid',
               takefocus=1, font=("Arial", 15, "bold"), width=15, height=2, border=0.5,
               command=self.lm.play.display).grid(row=1, column=0, columnspan=self.columns_count)
        #   Rules
        Button(self.lm, text="RÈGLES", activebackground=YELLOW, bg=YELLOW, fg=RED, activeforeground=RED,
               relief='solid', takefocus=1, font=("Arial", 15, "bold"), width=15, height=2,
               border=0.5, command=self.lm.rules.display)\
            .grid(row=2, column=0, columnspan=self.columns_count)

        #   "Made by ...":
        Label(self.lm, text="Made by \"Med-Studios\"", font=DEFAULT_FONT, bg=RED, fg="white")\
            .grid(row=self.rows_count-2, column=self.columns_count-1)
        #   Developers cards:
        self.load_image("resources/pictures/Dev.png", 1, RED).grid(row=self.rows_count-1, column=self.columns_count-1)
