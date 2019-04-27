from graphics.window import *
import game_system.player
import logging.config
import threading
import json
import signal
import os


def initialize_logger():
    """"Charge le logger"""
    config_path = 'resources/logging_config.json'
    logs_file_path = 'resources/appLogs.log'

    if os.path.exists(config_path):
        with open(config_path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
        print('Logger initialisé avec succès !')
    else:
        logging.basicConfig(level=logging.INFO)
        print('Initialisation du logger impossible ! Configuration par défaut définie !')

    if os.path.exists(logs_file_path):
        open(logs_file_path, 'w').close()


initialize_logger()

player = game_system.player.Player("lolilolulolilol", "127.0.0.1", -1)

windowThread = threading.Thread(target=run_window, name="WindowThread")
windowThread.start()
windowThread.join()

# Fermer le programme indépendamment des Threads lancés
os.kill(os.getpid(), signal.SIG_DFL)

"""
def run(action):
    asyncio.get_event_loop().run_until_complete(action)


def generate_server():
    global server
    server = unoserver.UnoServer()
    asyncio.get_event_loop().run_until_complete(server.create_server())


def generate_client():
    global client
    client = unoclient.UnoClient()
    client.connect_client()


def close_all():
    global client, server
    client.close()
    server.close()
    
generate_server()
generate_client()

while not client.is_connected():
    continue

client.get_client_transport().send_data(NewPlayerPacket(player))
"""