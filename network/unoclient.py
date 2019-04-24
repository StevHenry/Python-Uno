# -*- coding: utf-8 -*-

from network.unoconnection import *
import asyncio
import threading


class UnoClient(UnoConnectivity):
    __name__ = "UnoClient"

    def __init__(self, ip="0.0.0.0", default_port=8800):
        UnoConnectivity.__init__(self, ip=ip, default_port=default_port);
        self.close_connection = self.close
        self.is_connected = False
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def connect_client(self):
        self.port = self.default_port
        if str(self.ip) == "0.0.0.0":
            self.ip = "127.0.0.1"

        def connect(unoclient):
            client = ClientTransport(unoclient)
            coro = unoclient.loop.create_connection(lambda: client, unoclient.ip, unoclient.port)
            self.loop.run_until_complete(coro)

        self.connectionThread = threading.Thread(target=connect, args=(self,), name=(self.__name__ + str(self.port)))
        self.connectionThread.start()

    def is_connected(self):
        return self.is_connected

    def set_connected(self, is_connected_new_value):
        self.is_connected = is_connected_new_value

    async def handle_client(self):
        reader, writer = await asyncio.open_connection(self.ip, self.port, loop=self.loop)
        writer.write(b"Test")
        data = await reader.read()
        logger.debug('Received: %r' % data.decode())

    def close(self):
        try:
            self.client.close()
            logger.info("La connexion client au serveur a été fermée !")
        except AttributeError:
            logger.warning("La variable client est introuvable !")
        finally:
            self.loop.run_until_complete(self.client.wait_closed())
            self.loop.close()


class ClientTransport(asyncio.Protocol):
    def __init__(self, uno_client):
        self.uno_client = uno_client
        self.loop = uno_client.loop
        self.transport = None

    def disconnect(self):
        self.loop.stop()
        self.uno_client.set_connected(False)

    def connection_made(self, transport):
        self.transport = transport
        self.uno_client.set_connected(True)

    def data_received(self, data):
        logger.info('Data received from server: {}'.format(data.decode()))

    def send_data_to_tcp(self, data):
        self.transport.write(data.encode())

    def connection_lost(self, exc):
        logger.warn("Le serveur a fermé le serveur ! Fermeture du client ! ({})".format(str(exc)))
        self.loop.stop()
        self.uno_client.set_connected(False)
