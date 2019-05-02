from graphics.window import *
from tkinter import Label, Button, StringVar, Entry
from network import networkmanager


class PlayMenu(GridScene):
    def __init__(self):
        GridScene.__init__(self)

    def display(self):
        self.initialize_page("Sélection du serveur de jeu", 2, 4)

        Label(self.lm, text="⇒\tHéberger une partie\t⇐", font=("Trebuchet MS", 18), bg=LIGHT_RED, fg="white",
              borderwidth=0.5, relief="solid", height=2, width=60).grid(row=0, column=0)

        Button(self.lm, text="CRÉER UN SERVEUR", activebackground=YELLOW, bg=YELLOW, fg=RED, activeforeground=RED,
               relief='solid', takefocus=1, font=("Trebuchet MS", 15, "bold"), height=2, width=30, border=0.5,
               command=networkmanager.create_server).grid(row=1, column=0, rowspan=self.rows_count - 1)

        #LoadingPane(self, "TENTATIVATION")
        Label(self.lm, text="⇒\tRejoindre une partie\t⇐", font=("Trebuchet MS", 18), bg=LIGHT_RED, fg="white", height=2, width=60,
              borderwidth=0.5, relief="solid").grid(row=0, column=1)
        Button(self.lm, text="REJOINDRE UN SERVEUR", activebackground=YELLOW, bg=YELLOW, fg=RED, activeforeground=RED,
               relief='solid', takefocus=1, font=("Trebuchet MS", 15, "bold"), height=2, width=30, border=0.5,
               command=self.lm.game.display).grid(row=1, column=1, rowspan=self.rows_count - 1)

        Label(self.lm, text="ENTREZ UN PSEUDONYME:", font=("Arial", 12, "bold"), bg=RED, fg="white")\
            .grid(row=self.rows_count - 1, column=0, rowspan=2, columnspan=self.columns_count)
        Entry(self.lm, textvariable=StringVar(""), width=30).grid(row=self.rows_count, column=0,
                                                                  columnspan=self.columns_count)


class LoadingPane:
    def __init__(self, frame, loading_text):
        frame.title("UNO - Chargement...")
        for e in frame.grid_slaves():
            e.grid_forget()
        __columns_count = 3
        __rows_count = 4
        for k in range(__columns_count):
            frame.grid_columnconfigure(k, weight=1)
        for k in range(__rows_count):
            frame.grid_rowconfigure(k, weight=1)

        loading_gif = PhotoImage(file='resources/pictures/loading.gif')
        loading = Label(frame, image=loading_gif, borderwidth=0, highlightthickness=0, bg=TAPIS)
        loading.image = loading_gif
        loading.grid(row=2, column=0)

        Label(frame, text=loading_text, font=DEFAULT_FONT, bg=RED, fg=YELLOW).grid(row=1, column=1)