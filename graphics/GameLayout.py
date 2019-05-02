from graphics.window import *


class GameMenu(GridScene):
    def __init__(self):
        GridScene.__init__(self)

    def display(self):
        self.initialize_page("Partie", 5, 5)

        # Game:
        self.lm.configure(bg=TAPIS)

        # Dos Cartes:
        GridScene.load_image(self, 'resources/cards/I.png', 3, TAPIS).grid(row=2, column=0)
