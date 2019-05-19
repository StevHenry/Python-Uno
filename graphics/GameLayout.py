from graphics.window import *

player_hands = []


def get_player_hand(pseudo):
    for hand in player_hands:
        if hand.gamed_player.player.pseudonym == pseudo:
            return hand
    return None


class GamedPlayer:
    def __init__(self, player, position):
        self.player = player
        self.position = position


class GameMenu(GridScene):
    def __init__(self, frame):
        GridScene.__init__(self, frame)
        self.frame = frame

    def display(self):
        self.initialize_page(messages["window"]["game"]["name"], 5, 5)
        self.lm.uno_frame.protocol("WM_DELETE_WINDOW", game.ask_quit)
        # Game:
        self.lm.configure(bg=CARPET)

        self.load_image(game.last_played_card.texture_path, 5, CARPET).grid(row=2, column=1, columnspan=2)
        # Pioche:
        image2 = PhotoImage(file="resources/cards/Uno.png").subsample(5)
        button = Button(self.lm, image=image2, relief="solid", borderwidth=0, highlightthickness=0, bg=CARPET,
                        compound="center")
        button.image = image2
        button.grid(row=2, column=2, columnspan=2)

        # Return:
        image = PhotoImage(file="resources/pictures/Return.png").subsample(7)
        button = Button(self.lm, image=image, relief="solid", borderwidth=0, highlightthickness=0, bg=CARPET,
                        compound="center", command=game.ask_quit)
        button.image = image
        button.grid(row=0, column=0, sticky="nw")

        # Help:
        image = PhotoImage(file="resources/cards/I.png").subsample(8)
        button = Button(self.lm, image=image, relief="solid", borderwidth=0, highlightthickness=0, bg=CARPET,
                        compound="center", command=self.lm.rules.display)
        button.image = image
        button.grid(row=self.rows_count-1, column=self.columns_count-1, sticky="se")

        for k in range(5):
            self.lm.grid_columnconfigure(k, weight=1)
            self.lm.grid_rowconfigure(k, weight=1)


class PlayerHand(Frame):
    def __init__(self, pane, gamed_player):
        Frame.__init__(self, pane)
        self.gamed_player = gamed_player
        self.column = 1
        cspan = 1
        row = 1
        rspan = 1
        sticky="s"
        if gamed_player.position == "DOWN":
            cspan = 3
            row = 4
        elif gamed_player.position == "UP":
            cspan = 3
            row = 0
            sticky = "n"
        elif gamed_player.position == "LEFT":
            self.column = 0
            rspan = 3
            sticky = "w"
        else:
            self.column = 4
            rspan = 3
            sticky = "e"
        self.grid(column=self.column, columnspan=cspan, row=row, rowspan=rspan, padx=15, pady=45, sticky=sticky)

    def show(self):
        import time
        if self.gamed_player.position == "DOWN":
            for card in self.gamed_player.player.player_hand:
                self.load_button(card.texture_path, 4, CARPET, command=lambda: logger.debug("CLICKED!")).pack(side="left")
                time.sleep(0.1)
        else:
            for i in range(len(self.gamed_player.player.player_hand)):
                if self.gamed_player.position == "RIGHT":
                    if i > 1:
                        self.load_image("resources/cards/Uno_right.png", 7, CARPET).pack()
                elif self.gamed_player.position == "UP":
                    self.load_image("resources/cards/Uno.png", 7, CARPET).pack(side="left")
                elif self.gamed_player.position == "LEFT":
                    if i > 1:
                        self.load_image("resources/cards/Uno_right.png", 7, CARPET).pack()
                time.sleep(0.1)

    def load_image(self, path, divisor, background):
        image = PhotoImage(file=path)
        if divisor > 0:
            image = image.subsample(divisor)
        image_label = Label(self, image=image, borderwidth=0, highlightthickness=0, bg=background)
        image_label.image = image
        return image_label

    def load_button(self, path, divisor, background, command=None):
        image = PhotoImage(file=path)
        if divisor > 0:
            image = image.subsample(divisor)
        imaged_button = Button(self, image=image, borderwidth=0, highlightthickness=0, bg=background, command=command)
        imaged_button.image = image
        return imaged_button
