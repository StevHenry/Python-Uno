# -*- coding: utf-8 -*-

from network.unoconnection import *
import asyncio
import logging
import threading

logger = logging.getLogger(__name__)
players = []


class UnoServer(UnoConnectivity):
    __name__ = "UnoServer"

    def __init__(self, ip="0.0.0.0", default_port=8800):
        UnoConnectivity.__init__(self, ip=ip, default_port=default_port);
        self.close_connection = self.close
        self.loop = asyncio.new_event_loop()
        self.server = None

    async def create_server(self):
        """" Générer le serveur sur une intervalle de port entre 'default_port' et 'default_port'+10 """
        globals()

        logger.info("Looking for an available port")
        for additive in range(1):
            is_free = await check_port(self, self.default_port + additive)
            if is_free:
                logger.info("Port libre trouvé: %r" % str(self.default_port + additive))
                self.port = self.default_port + additive
                break

        if self.port == 0:
            logger.info("No available port could be found ! Trying to force on default_port (%r) !" % self.default_port)
            self.port = self.default_port

        self.connectionThread = threading.Thread(target=self.run_server, name=(self.__name__ + str(self.port)))
        self.connectionThread.start()

    def run_server(self):
        """ Fonction qui démarre le serveur """
        asyncio.set_event_loop(self.loop)
        coro = self.loop.create_server(ServerTransport, self.ip, self.port)
        self.server = self.loop.run_until_complete(coro)
        logger.info('Serveur démarré sur {}'.format(self.server.sockets[0].getsockname()))

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

    @asyncio.coroutine
    async def server_handle(self, reader, writer):
        data = await reader.read()
        packet = data.decode()
        client_address = writer.get_extra_info('peername')
        logger.debug("Message reçu: %r" % packet)
        logger.info("Nouveau client à l'adresse %r" % str(client_address))
        message = "Salut"
        logger.info("Envoi de: %r" % message)
        writer.write(bytes(message, encoding="utf-8"))
        await writer.drain()

        logger.info("Fermeture de la connexion")
        writer.close()

    def close(self):
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.close()
        logger.info("Le serveur a été fermé !")


class ServerTransport(asyncio.Transport):
    globals()

    def __init__(self):
        self.transport = None
    
    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        logger.info("Nouvelle connexion à l'adresse: {}".format(peername))

    def data_received(self, msg):
        logger.info("Reçu: {0} de: {1}".format(msg, self.transport.get_extra_info('peername')))

    def write(self, data):
        self.transport.write(bytes(data, encoding="utf-8"))
        logger.debug("Sent {0} to {1}".format(data, self.transport.get_extra_info('peername')))
