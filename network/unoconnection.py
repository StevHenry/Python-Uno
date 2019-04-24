# -*- coding: utf-8 -*-

import asyncio
import socket
import logging
from network import unoconnection

logger = logging.getLogger(__name__)


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

    def get_port(self):
        return self.port


async def check_port(cls, tested_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex((cls.ip, tested_port))
        sock.close()
        if result == 0:
            logger.debug("connect_ex result: 0")
            return True
        elif result == 10049:
            logger.info("Defined IP (%r) is invalid ! Changed to 127.0.0.1 !" % cls.ip)
            cls.ip = "127.0.0.1"
            return await check_port(cls, tested_port)
        elif result == 10061:
            logger.debug("Error 10061 when trying to check port on (%r, %r) !" % (cls.ip, tested_port))
            return False
        else:
            logger.debug("connect_ex result: %r" % result)
            return False
