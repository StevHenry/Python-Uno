# -*- coding: utf-8 -*-

from tkinter import *
import logging

logger = logging.getLogger(__name__)


class HomeGrid(Frame):
    globals()
    columns_count = 3
    rows_count = 6

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.__layout_configuration()

        for k in range(HomeGrid.columns_count-1):
            self.grid_columnconfigure(k, weight=1)
        for k in range(HomeGrid.rows_count-1):
            self.grid_rowconfigure(k, weight=1)

        #   Logo:
        uno = PhotoImage(file='resources/pictures/Logo (2).png')
        uno_img = Label(self, image=uno, borderwidth=0, highlightthickness=0)
        uno_img.image = uno
        uno_img.grid(row=0, column=0, rowspan=1, columnspan=HomeGrid.columns_count)

        # Buttons:
        play = Button(self, text="JOUER", activebackground='#febe2e', activeforeground='#ed2600', bg='#febe2e',
                      fg='#ed2600', relief='solid', takefocus=1, font=("Courier New Bold", 15, 'bold'), width=15,
                      height=2, border=0.5, command=self.print_pseudo)
        play.grid(row=1, column=0, rowspan=1, columnspan=HomeGrid.columns_count)

        rules_button = Button(self, text="RÈGLES", activebackground='#febe2e', activeforeground='#ed2600', bg='#febe2e',
                              fg='#ed2600', relief='solid', takefocus=1, font=('arial', 15, 'bold'), width=15, height=2,
                              border=0.5, command=change_to_rules)
        rules_button.grid(row=2, column=0, rowspan=1, columnspan=HomeGrid.columns_count)

        # "Made by ...":
        made_by = Label(self, text="Made by \"Med-Studios\"", font=("Arial", 14, "italic bold"),
                        bg='#ed2600', fg='#ffffff')
        made_by.grid(row=HomeGrid.rows_count - 2, column=HomeGrid.columns_count - 1)

        #   Dev cards:
        dev_cards_image = PhotoImage(file='resources/pictures/Dev.png')
        dev_cards = Label(self, image=dev_cards_image, borderwidth=0, highlightthickness=0)
        dev_cards.image = dev_cards_image
        dev_cards.grid(row=HomeGrid.rows_count - 1, column=HomeGrid.columns_count - 1)

        # Pseudo:
        global value
        value = StringVar(value="Player")
        entree = Entry(self, textvariable=value, width=30)
        entree.grid(row=HomeGrid.rows_count - 1, column=0)

    def __layout_configuration(self):
        self.configure(bg='#ed2600')
        self.grid(sticky="nsew")

    @staticmethod
    def print_pseudo():
        global value
        logger.debug("Pseudo choisi: %r" % value.get())


def change_to_rules():
    pass


def run_window():
    global window
    window = Tk()
    window.state('zoomed')
    window.minsize(900, 600)
    window.title("UNO")
    window.grid_propagate(0)
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)
    HomeGrid(window)
    window.mainloop()
