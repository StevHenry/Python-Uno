from network.networkmanager import NetworkManager as nw
import os
import json
import logging.config
from player import Player


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

playerPseudo = "lolilolulolilol"

server = nw(is_client_connection=False)
server.run()

client = nw(chosen_port=8800)
client.run()
