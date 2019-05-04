# -*- coding: utf-8 -*-

from network.unoconnection import *
from network.unopacket import UnoPacket
import logging
import asyncio
import threading


logger = logging.getLogger(__name__)


class UnoClient(UnoConnectivity):
    __name__ = "UnoClient"

    def __init__(self, ip="0.0.0.0", default_port=8800):
        UnoConnectivity.__init__(self, ip=ip, default_port=default_port)
        self.connectionThread = threading.Thread(target=self.__connect, name=(self.__name__ + str(self.port)))
        self.close_connection = self.__close
        self.loop = asyncio.new_event_loop()
        self.is_linked = False
        self.connection_error = None

    def connect_client(self):
        self.port = self.default_port
        if str(self.ip) == "0.0.0.0":
            self.ip = "127.0.0.1"

        self.connectionThread.start()

    def __connect(self):
        try:
            self.client = ClientTransport(self)
            asyncio.set_event_loop(self.loop)
            coro = self.loop.create_connection(lambda: self.client, self.ip, self.port)
            self.loop.run_until_complete(coro)
        except ConnectionRefusedError as e:
            logger.debug("Client connection to provided server is impossible !")
            self.connection_error = e

    def __close(self):
        if self.is_linked:
            self.client.disconnect(self.loop)
            logger.info("La connexion client au serveur a été fermée !")
        else:
            logger.debug("La connexion client au serveur est inexistante ! Impossible de la fermer !")

    def is_connected(self):
        return self.is_linked

    def set_connected(self, is_connected_new_value):
        self.is_linked = is_connected_new_value

    def get_client_transport(self):
        return self.client


class ClientTransport(asyncio.Protocol):
    def __init__(self, uno_client):
        self.uno_client = uno_client
        self.loop = uno_client.loop
        self.transport = None

    def disconnect(self, loop):
        self.transport.close()
        loop.close()
        self.uno_client.set_connected(False)

    def connection_made(self, transport):
        self.transport = transport
        self.uno_client.set_connected(True)

    def data_received(self, data):
        logger.info('Data received from server: {}'.format(data.decode()))

    def send_data(self, packet):
        if not isinstance(packet, UnoPacket):
            raise ValueError("Specified data to send is not a Packet !")
        self.transport.write(bytes(packet.data, encoding="utf-8"))

    def connection_lost(self, exc):
        logger.warning("Le serveur a fermé le serveur ! Fermeture du client ! ({})".format(str(exc)))
        self.loop.stop()
        self.uno_client.set_connected(False)
