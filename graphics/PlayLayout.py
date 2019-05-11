from graphics.window import *
from tkinter import StringVar, Entry
import re

ip_var = StringVar(value="127.0.0.1")
port_var = StringVar(value="8800")
pseudonym = StringVar(value=game.my_player.pseudonym)


class PlayMenu(GridScene):
    def __init__(self, frame):
        GridScene.__init__(self, frame)
        self.error = None

    def display(self):
        self.initialize_page(messages["window"]["play"]["name"], 5, 9)

        #   Logo:
        self.load_image("resources/pictures/Logo (2).png", 1, RED).grid(row=0, column=0, columnspan=self.columns_count)

        Button(self.lm, text=messages["window"]["play"]["create_server"], activebackground=YELLOW, bg=YELLOW, fg=RED,
               activeforeground=RED, relief='solid', takefocus=1, font=("Trebuchet MS", 13, "bold"), height=2, width=30,
               border=0.5, command=ConfigureServerPane(self).display).grid(row=1, column=1)

        Button(self.lm, text=messages["window"]["play"]["join_server"], activebackground=YELLOW, bg=YELLOW, fg=RED,
               activeforeground=RED, relief='solid', takefocus=1, font=("Trebuchet MS", 13, "bold"), height=2, width=30,
               border=0.5, command=SelectServerPane(self).display).grid(row=1, column=3)

        Label(self.lm, text=messages["window"]["play"]["type_pseudo"], font=("Arial", 12, "bold"), bg=RED, fg="white") \
            .grid(row=5, column=0, columnspan=self.columns_count)

        Entry(self.lm, textvariable=pseudonym, width=30).grid(row=6, column=0,
                                                              columnspan=self.columns_count)

        if self.error is not None:
            Label(self.lm, text=self.error, font=("Arial", 12, "bold"), bg=RED, fg="white") \
                .grid(row=2, rowspan=2, column=0, columnspan=self.columns_count)
            self.error = None

        # Return:
        image = PhotoImage(file="resources/pictures/Return.png").subsample(6)
        button = Button(self.lm, image=image, relief="solid", borderwidth=0, highlightthickness=0, bg=RED,
                        command=self.lm.home.display, compound="center")
        button.image = image
        button.grid(row=self.rows_count - 1, column=0, columnspan=self.columns_count)


class LoadingPane:
    def __init__(self, scene, text, action_method):
        self.scene = scene
        self.text = text
        self.execution = action_method

    def display(self):
        GridScene.initialize_page(self.scene, messages["window"]["loading"]["name"], 3, 8)
        Label(self.scene.lm, text=self.text, font=DEFAULT_FONT, bg=RED, fg=YELLOW).grid(row=5, column=1)
        GridScene.load_gif(self.scene, "resources/pictures/loading_little.gif", RED).grid(row=4, column=1)
        check_client = threading.Thread(target=self.execution, name="ClientConnectionChecker")
        check_client.start()


class SelectServerPane:
    def __init__(self, scene):
        self.scene = scene

    def display(self):
        if not check_pseudonym():
            return
        GridScene.initialize_page(self.scene, messages["window"]["server"]["joining"]["name"], 5, 6)

        Label(self.scene.lm, text=messages["window"]["server"]["joining"]["title"], font=("Arial", 18, "bold"), bg=RED, fg=YELLOW) \
            .grid(row=0, column=0, columnspan=self.scene.columns_count)

        Label(self.scene.lm, text=messages["window"]["server"]["joining"]["ip"], font=("Arial", 14, "bold"), bg=RED, fg="white") \
            .grid(row=1, column=0, columnspan=2)
        Entry(self.scene.lm, textvariable=ip_var, width=60).grid(row=1, column=2, columnspan=3)

        Label(self.scene.lm, text=messages["window"]["server"]["joining"]["port"], font=("Arial", 14, "bold"), bg=RED, fg="white") \
            .grid(row=2, column=0, columnspan=2)
        Entry(self.scene.lm, textvariable=port_var, width=60).grid(row=2, column=2, columnspan=3)

        Button(self.scene.lm, text=messages["window"]["server"]["joining"]["execute"], activebackground=YELLOW, bg=YELLOW, fg=RED, activeforeground=RED,
               relief='solid', takefocus=1, font=("Trebuchet MS", 15, "bold"), height=2, width=30, border=0.5,
               command=LoadingPane(self.scene, messages["window"]["loading"]["server_joining"], self.try_client_connection).display) \
            .grid(row=self.scene.rows_count - 1, column=0, columnspan=self.scene.columns_count)

    @staticmethod
    def try_client_connection():
        if not re.compile("[\\S]+").match(ip_var.get()):
            logger.debug("L'IP spécifiée n'est pas correcte!")
            not_connected(messages["error"]["configuration"]["ip"])
            return
        try:
            int(port_var.get())
        except ValueError:
            logger.debug("Le port spécifié n'est pas correct!")
            not_connected(messages["error"]["configuration"]["port"])
            return

        logger.debug("IP, port: OK")

        try:
            nm.connect_client(str(ip_var.get()), int(port_var.get().replace(" ", "")))
        except Exception as e:
            not_connected(e)

        laps = 0
        while True:
            if nm.client.connection_error:
                not_connected(str(nm.client.connection_error))
                break
            elif nm.client.is_connected():
                connected()
                break
            else:
                if laps <= 20:
                    time.sleep(0.5)
                    laps += 1
                else:
                    not_connected(messages["error"]["timeout"])
                    break


class ConfigureServerPane:
    def __init__(self, scene):
        self.scene = scene

    def display(self):
        if not check_pseudonym():
            return
        global port_var
        GridScene.initialize_page(self.scene, messages["window"]["server"]["hosting"]["name"], 3, 4)

        Label(self.scene.lm, text=messages["window"]["server"]["hosting"]["title"], font=("Arial", 18, "bold"), bg=RED, fg=YELLOW) \
            .grid(row=0, column=0, columnspan=self.scene.columns_count)

        Label(self.scene.lm, text=messages["window"]["server"]["hosting"]["port"], font=("Arial", 14, "bold"), bg=RED, fg="white") \
            .grid(row=1, column=0, columnspan=self.scene.columns_count)
        Entry(self.scene.lm, textvariable=port_var, width=20).grid(row=1, column=0, columnspan=self.scene.columns_count,
                                                                   rowspan=2)

        Button(self.scene.lm, text=messages["window"]["server"]["hosting"]["execute"], activebackground=YELLOW, bg=YELLOW, fg=RED, activeforeground=RED,
               relief='solid', takefocus=1, font=("Trebuchet MS", 15, "bold"), height=2, width=30, border=0.5,
               command=self.start).grid(row=self.scene.rows_count - 1, column=0, columnspan=self.scene.columns_count)

    def start(self):
        try:
            int(port_var.get())
            logger.debug("Port: OK")
        except ValueError:
            logger.debug("Le port spécifié n'est pas correct!")
            not_connected(messages["error"]["configuration"]["port"])
            return

        LoadingPane(self.scene, messages["window"]["loading"]["server_joining"], self.run_server_and_connect).display()

    @staticmethod
    def run_server_and_connect():
        try:
            nm.create_server("127.0.0.1", int(port_var.get().replace(" ", "")))
            nm.connect_client("127.0.0.1", int(port_var.get().replace(" ", "")))
        except Exception as e:
            not_connected(e)

        laps = 0
        while True:
            if nm.client.connection_error:
                not_connected(str(nm.client.connection_error))
                break
            elif nm.client.is_connected():
                connected()
                break
            else:
                if laps <= 20:
                    time.sleep(0.5)
                    laps += 1
                else:
                    not_connected("Timeout !")
                    break


def check_pseudonym():
    if re.compile("^[\\s]+$|#|^$").match(pseudonym.get()):
        logger.debug("Le pseudo spécifié n'est pas correct !")
        not_connected(messages["error"]["configuration"]["pseudo"])
    else:
        game.my_player.pseudonym = pseudonym.get()
        return True
    return False


def connected():
    from graphics.window import layout_manager
    nm.client_success_connect()
    layout_manager.waiting_room.display()


def not_connected(message):
    from graphics.window import layout_manager
    layout_manager.play.error = message
    layout_manager.play.display()
