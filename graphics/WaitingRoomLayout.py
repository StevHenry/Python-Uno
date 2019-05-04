from graphics.window import *


class WaitingRoom(GridScene):
    def __init__(self):
        GridScene.__init__(self)
        self.ip = None
        self.port = 0
        self.players = None
        self.set_players("lolilolulolilol#HEY#It's me")

    def set_ip_port(self, ip, port):
        self.ip = ip
        self.port = port

    def set_players(self, players):
        self.players = players

    def display(self):
        self.initialize_page("Salle d'attente", 5, 5)

        Label(self.lm, text="- " + self.players.replace("#", "\n-") if self.players is not None else "", font=("Trebuchet MS", 18), bg=LIGHT_RED, fg="white",
              borderwidth=0.5, relief="solid", width=60, height=12)\
            .grid(row=2, column=1, columnspan=3, rowspan=self.rows_count-2)

        Label(self.lm, text="SALLE D'ATTENTE:", font=("Trebuchet MS", 18, "underline"), bg=RED, fg="white")\
            .grid(row=0, column=0, columnspan=2)
        Label(self.lm, text="Serveur {0}:{1}\nHôte: {2}".format(self.ip, self.port, "PSEUDO HOTE"), font=("Trebuchet MS", 14, "italic"), bg=RED,
              fg=YELLOW).grid(row=0, column=3, columnspan=2)
