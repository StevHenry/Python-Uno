from graphics.window import *
from tkinter import Label, Button, PhotoImage


class RulesMenu(GridScene):
    def __init__(self):
        GridScene.__init__(self)

    def display(self):
        self.initialize_page("Règles", 3, 6)

        rules_text = open('resources/rules1.txt', 'r', encoding="utf-8").read()
        Label(self.lm, text="RÈGLES", font=("Arial", 18, "bold underline"), bg=RED, fg=YELLOW).grid(row=1, column=1)
        Label(self.lm, text=rules_text, font=("Arial", 16, "bold"), bg=RED, fg=YELLOW).grid(row=2, column=1)

        Label(self.lm, text="\nCARTES SPÉCIALES", font=("Arial", 18, "bold underline"), bg=RED, fg=YELLOW)\
            .grid(row=self.rows_count - 3, column=1)
        rules_two_text = open('resources/rules2.txt', 'r', encoding="utf-8").read()
        Label(self.lm, text=rules_two_text, font=("Arial", 16, "bold"), bg=RED, fg=YELLOW)\
            .grid(row=self.rows_count - 2, column=1)

        # Cards:
        self.load_image("resources/cards/I.png", 5, RED).grid(row=0, column=0, sticky="nw")
        self.load_image("resources/cards/I.png", 5, RED).grid(row=self.rows_count - 1, column=0, sticky="sw")
        self.load_image("resources/cards/I.png", 5, RED).grid(row=0, column=self.columns_count - 1, sticky="en")
        self.load_image("resources/cards/I.png", 5, RED)\
            .grid(row=self.rows_count - 1, column=self.columns_count - 1, sticky="se")

        # Return:
        image = PhotoImage(file="resources/pictures/Return.png").subsample(4)
        button = Button(self.lm, image=image, relief="solid", borderwidth=1, highlightthickness=0, bg=RED,
                        command=self.lm.home.display, compound="center")
        button.image = image

        button.grid(row=self.rows_count-1, column=1)
