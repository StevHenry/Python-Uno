# -*- coding: utf-8 -*-

from tkinter import Tk, Frame, Label, Button, PhotoImage, StringVar, Entry
from tkinter import messagebox
from network import networkmanager
import threading
import logging

logger = logging.getLogger(__name__)
RED = "#ed2600"
LIGHT_RED = "#e84a4a"
YELLOW = "#febe2e"
DEFAULT_FONT = ("Arial", 14, "italic bold")


class GridManager(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.configure(bg='#ed2600')
        self.grid(sticky="nsew")

    def home_grid(self):
        window.title("UNO - Menu principal")
        for e in self.grid_slaves():
            e.grid_forget()

        __columns_count = 3
        __rows_count = 6
        for k in range(__columns_count - 1):
            self.grid_columnconfigure(k, weight=1)
        for k in range(__rows_count - 1):
            self.grid_rowconfigure(k, weight=1)

        #   Logo:
        uno_image = PhotoImage(file='resources/pictures/Logo (2).png')
        uno = Label(self, image=uno_image, borderwidth=0, highlightthickness=0)
        uno.image = uno_image
        uno.grid(row=0, column=0, columnspan=__columns_count)

        # Buttons:
        Button(self, text="JOUER", activebackground=YELLOW, bg=YELLOW, fg=RED, activeforeground=RED, relief='solid',
               takefocus=1, font=("Arial", 15, "bold"), width=15, height=2, border=0.5,
               command=self.play_menu).grid(row=1, column=0, columnspan=__columns_count)
        # Rules
        Button(self, text="RÈGLES", activebackground=YELLOW, bg=YELLOW, fg=RED, activeforeground=RED,
               relief='solid', takefocus=1, font=("Arial", 15, "bold"), width=15, height=2,
               border=0.5).grid(row=2, column=0, columnspan=__columns_count)
        # "Made by ...":
        Label(self, text="Made by \"Med-Studios\"", font=DEFAULT_FONT, bg=RED, fg="white")\
            .grid(row=__rows_count - 2, column=__columns_count - 1)
        #   Dev cards:
        dev_cards_image = PhotoImage(file='resources/pictures/Dev.png')
        dev_cards = Label(self, image=dev_cards_image, borderwidth=0, highlightthickness=0)
        dev_cards.image = dev_cards_image
        dev_cards.grid(row=__rows_count - 1, column=__columns_count - 1)

    def play_menu(self):
        window.title("UNO - Sélection du serveur")
        for e in self.grid_slaves():
            e.grid_forget()
        __columns_count = 2
        __rows_count = 4
        for k in range(__columns_count):
            self.grid_columnconfigure(k, weight=1)
        for k in range(__rows_count):
            self.grid_rowconfigure(k, weight=1)

        Label(self, text="⇒\tHéberger une partie\t⇐", font=("Trebuchet MS", 18), bg=LIGHT_RED, fg="white",
              borderwidth=0.5, relief="solid", height=2, width=60).grid(row=0, column=0)

        Button(self, text="CRÉER UN SERVEUR", activebackground=YELLOW, bg=YELLOW, fg=RED, activeforeground=RED,
               relief='solid', takefocus=1, font=("Trebuchet MS", 15, "bold"), height=2, width=30, border=0.5,
               command=networkmanager.create_server).grid(row=1, column=0, rowspan=__rows_count-1)

        Label(self, text="⇒\tRejoindre une partie\t⇐", font=("Trebuchet MS", 18), bg=LIGHT_RED, fg="white", height=2, width=60,
              borderwidth=0.5, relief="solid").grid(row=0, column=1)
        Button(self, text="REJOINDRE UN SERVEUR", activebackground=YELLOW, bg=YELLOW, fg=RED, activeforeground=RED,
               relief='solid', takefocus=1, font=("Trebuchet MS", 15, "bold"), height=2, width=30, border=0.5,
               command=networkmanager.connect_client).grid(row=1, column=1, rowspan=__rows_count-1)

        Label(self, text="Entrez votre pseudonyme:\n(Celui-ci sera utilisé en jeu!)", font=("Arial", 12, "bold"), bg=RED, fg="white")\
            .grid(row=__rows_count-1, column=0, rowspan=2, columnspan=__columns_count)
        global value
        Entry(self, textvariable=value, width=30).grid(row=__rows_count, column=0, columnspan=__columns_count)

    @staticmethod
    def print_pseudo():
        global value
        logger.debug("Pseudo choisi: %r" % value.get())


def initialize_window():
    global window, value
    window = Tk()
    window.state('zoomed')
    window.minsize(900, 600)
    window.protocol("WM_DELETE_WINDOW", ask_quit)
    window.grid_propagate(0)
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)
    value = StringVar(value="Pseudonyme")

    GridManager(window).home_grid()


def run_window():
    global window
    initialize_window()
    window.mainloop()


def ask_quit():
    def ask():
        if messagebox.askyesno("Quitter UNO", "Voulez-vous vraiment quitter? ⊙_⊙", icon=messagebox.WARNING):
            global window
            window.destroy()

    threading.Thread(target=ask, name="QuitThread").start()
