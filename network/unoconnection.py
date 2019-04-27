# -*- coding: utf-8 -*-

import asyncio
import socket
import logging


class UnoConnectivity(object):
    """ Objet UnoConnectivity """
    globals()

    def __new__(cls, ip="0.0.0.0", default_port=8800):
        return super().__new__(cls)

    def __init__(self, ip="0.0.0.0", default_port=8800):
        """ Initialiser les variables par défaut du serveur """
        self.ip = ip
        self.port = 0
        self.default_port = default_port
        self.connectionThread = None
        self.new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.new_loop)

    def close_connection(self):
        pass
