from graphics.window import *
from network import networkmanager as nm


class GameMenu(GridScene):
    def __init__(self, frame):
        GridScene.__init__(self, frame)

    def display(self):
        self.initialize_page(messages["window"]["game"]["name"], 11, 5)
        self.lm.uno_frame.protocol("WM_DELETE_WINDOW", self.ask_quit)
        # Game:
        self.lm.configure(bg=CARPET)

        # Pioche:

        # Return:
        image = PhotoImage(file="resources/pictures/Return.png").subsample(6)
        button = Button(self.lm, image=image, relief="solid", borderwidth=0, highlightthickness=0, bg=CARPET,
                        compound="center", command=self.ask_quit)
        button.image = image
        button.grid(row=0, column=0)

        self.load_image("resources/cards/Uno.png", 5, CARPET).grid(row=3, column=4)

    def ask_quit(self):
        def ask():
            if messagebox.askyesno(messages["quit"]["name"], messages["quit"]["question_host"] if nm.is_host else
                                                            messages["quit"]["question"], icon=messagebox.WARNING):
                self.lm.home.display()
                nm.client.close_connection()
                if nm.is_host:
                    nm.server.close_connection(messages["error"]["host_ended_game"])
        threading.Thread(target=ask, name="QuitThread").start()
