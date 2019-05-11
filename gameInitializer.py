# -*- coding: utf-8 -*-

import uno_messages
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
        logging.getLogger("loggerInitialize").debug("Logger initialisé avec succès !")
    else:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger("loggerInitialize").debug("Initialisation du logger impossible ! Configuration par défaut définie !")

    if os.path.exists(logs_file_path):
        open(logs_file_path, 'w').close()


initialize_logger()
uno_messages.initialize_messages_config()

from graphics.window import run_window
from network import networkmanager

windowThread = threading.Thread(target=run_window, name="WindowThread")
windowThread.start()
windowThread.join()

#   Fermer clients/serveurs
if networkmanager.client is not None and networkmanager.client.is_connected():
    networkmanager.client.close_connection()
if networkmanager.server is not None and networkmanager.server.loop.is_running():
    networkmanager.server.close_connection(uno_messages.messages["error"]["server_closed_by_host"])

# Fermer le programme
os.kill(os.getpid(), signal.SIG_DFL)
