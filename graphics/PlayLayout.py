from graphics.window import *
from tkinter import Label, Button, StringVar, Entry


class PlayMenu(GridScene):
    def __init__(self):
        GridScene.__init__(self)

    def display(self):
        self.initialize_page("Sélection du serveur de jeu", 2, 4)

        Label(self.lm, text="⇒\tHéberger une partie\t⇐", font=("Trebuchet MS", 18), bg=LIGHT_RED, fg="white",
              borderwidth=0.5, relief="solid", height=2, width=60).grid(row=0, column=0)

        Button(self.lm, text="CRÉER UN SERVEUR", activebackground=YELLOW, bg=YELLOW, fg=RED, activeforeground=RED,
               relief='solid', takefocus=1, font=("Trebuchet MS", 15, "bold"), height=2, width=30, border=0.5,
               command=ClientLoadingPane(self).display).grid(row=1, column=0, rowspan=self.rows_count - 1)

        Label(self.lm, text="⇒\tRejoindre une partie\t⇐", font=("Trebuchet MS", 18), bg=LIGHT_RED, fg="white", height=2, width=60,
              borderwidth=0.5, relief="solid").grid(row=0, column=1)
        Button(self.lm, text="REJOINDRE UN SERVEUR", activebackground=YELLOW, bg=YELLOW, fg=RED, activeforeground=RED,
               relief='solid', takefocus=1, font=("Trebuchet MS", 15, "bold"), height=2, width=30, border=0.5,
               command=JoinServerPane(self).display).grid(row=1, column=1, rowspan=self.rows_count - 1)

        Label(self.lm, text="ENTREZ UN PSEUDONYME:", font=("Arial", 12, "bold"), bg=RED, fg="white")\
            .grid(row=self.rows_count - 1, column=0, rowspan=2, columnspan=self.columns_count)
        Entry(self.lm, textvariable=StringVar(""), width=30).grid(row=self.rows_count, column=0,
                                                                  columnspan=self.columns_count)


class ClientLoadingPane:
    def __init__(self, scene):
        self.scene = scene

    def display(self):
        GridScene.initialize_page(self.scene, "Chargement...", 3, 8)
        Label(self.scene.lm, text="Connexion au serveur ...", font=DEFAULT_FONT, bg=RED, fg=YELLOW).grid(row=5, column=1)
        GridScene.load_gif(self.scene, "resources/pictures/loading_little.gif", RED).grid(row=4, column=1)

        def check_for_connection(cls):
            from network import networkmanager
            networkmanager.create_server()
            networkmanager.connect_client()

            import time
            times = 0
            while True:
                if networkmanager.client.connection_error:
                    cls.not_connected(str(networkmanager.client.connection_error))
                    break
                elif networkmanager.client.is_connected():
                    cls.connected()
                    break
                else:
                    if times <= 20:
                        time.sleep(0.5)
                        times += 1
                    else:
                        cls.not_connected("Timeout !")
                        break
        check_client = threading.Thread(target=check_for_connection, args=(self,), name="ClientConnectionChecker")
        check_client.start()

    def connected(self):
        from network import networkmanager
        self.scene.lm.waiting_room.set_ip_port(networkmanager.server.ip, networkmanager.server.port)
        self.scene.lm.waiting_room.display()

    def not_connected(self, message):
        logger.debug("NOT CONNECTED! (%r)" % message)


class JoinServerPane:
    def __init__(self, scene):
        self.scene = scene

    def display(self):
        global ip_var, port_var
        GridScene.initialize_page(self.scene, "Rejoindre une partie...", 5, 6)

        Label(self.scene.lm, text="⇒\tRejoindre une partie\t⇐", font=("Trebuchet MS", 18), bg=LIGHT_RED, fg="white",
              borderwidth=0.5, relief="solid", height=2, width=120).grid(row=0, column=0,
                                                                        columnspan=self.scene.columns_count)
        ip_var = StringVar(value="127.0.0.1")
        port_var = StringVar(value="8800")

        Label(self.scene.lm, text="IP du serveur:", font=("Arial", 12, "bold underline"), bg=RED, fg="white")\
            .grid(row=1, column=0, columnspan=2)
        Entry(self.scene.lm, textvariable=ip_var, width=60).grid(row=1, column=2, columnspan=3)

        Label(self.scene.lm, text="Port du serveur:", font=("Arial", 12, "bold underline"), bg=RED, fg="white")\
            .grid(row=2, column=0, columnspan=2)
        Entry(self.scene.lm, textvariable=port_var, width=60).grid(row=2, column=2, columnspan=3)

        Button(self.scene.lm, text="Connexion", activebackground=YELLOW, bg=YELLOW, fg=RED, activeforeground=RED,
               relief='solid', takefocus=1, font=("Trebuchet MS", 15, "bold"), height=2, width=30, border=0.5,
               command=ClientLoadingPane(self.scene).display)\
            .grid(row=self.scene.rows_count-1, column=0, columnspan=self.scene.columns_count)
