from graphics.window import *


class WaitingRoom(GridScene):
    def __init__(self, frame):
        GridScene.__init__(self, frame)
        self.players = None

    def display(self):
        self.initialize_page(messages["window"]["waiting_room"]["name"], 5, 5)
        self.lm.uno_frame.protocol("WM_DELETE_WINDOW", self.ask_quit)
        Label(self.lm, text=messages["window"]["waiting_room"]["players_display"].format(len(game.players_in_game)) +
              "\n\n- " + "\n- ".join(game.players_in_game),
              font=("Trebuchet MS", 18), bg=LIGHT_RED, fg="white", borderwidth=0.5, relief="solid", width=60,
              height=12).grid(row=1, column=1, columnspan=3, rowspan=self.rows_count - 2)

        Label(self.lm, text=messages["window"]["waiting_room"]["title"], font=("Trebuchet MS", 18, "bold"), bg=RED,
              fg="white") \
            .grid(row=0, column=0, columnspan=2)
        Label(self.lm,
              text=messages["window"]["waiting_room"]["server_info"].format(nm.client.ip, nm.client.port,
                                                                            game.game_host,
                                                                            game.my_player.pseudonym), bg=RED,
              font=("Trebuchet MS", 14, "italic"), fg=YELLOW).grid(row=0, column=3, columnspan=2)

        if nm.is_host:
            if len(game.players_in_game) < 2:
                Button(self.lm, text=messages["window"]["waiting_room"]["begin"]["host_less"].format(4 - len(game.players_in_game)),
                       activebackground=YELLOW, bg=YELLOW, activeforeground=RED, relief='solid', takefocus=1, fg=RED,
                       font=("Arial", 15, "bold"), height=2, border=0.5, state="disabled") \
                    .grid(row=4, column=0, columnspan=self.columns_count)

            else:
                Button(self.lm, text=messages["window"]["waiting_room"]["begin"]["host_valid"], fg=RED, activebackground=YELLOW, bg=YELLOW, activeforeground=RED,
                       width=15, relief='solid', takefocus=1, font=("Arial", 15, "bold"), height=2, border=0.5,
                       command=game.server_game_start).grid(row=4, column=0, columnspan=self.columns_count)
        else:
            Label(self.lm, text=messages["window"]["waiting_room"]["begin"]["client"], font=("Trebuchet MS", 12, "bold"),
                  bg=RED, fg="white").grid(row=4, column=0, columnspan=self.columns_count)

    def ask_quit(self):
        def ask():
            if messagebox.askyesno(messages["quit"]["name"], messages["quit"]["question_host"] if nm.is_host else
                                                            messages["quit"]["question"], icon=messagebox.WARNING):
                self.lm.home.display()
                nm.client.close_connection()
                if nm.is_host:
                    nm.server.close_connection(messages["error"]["host_ended_game"])
        threading.Thread(target=ask, name="QuitThread").start()