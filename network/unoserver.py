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
        self.loop = asyncio.new_event_loop()
        self.close_connection = self.__close
        self.server = None

    async def create_server(self):
        """" Générer le serveur sur une intervalle de port entre 'default_port' et 'default_port'+10 """
        globals()

        logger.info("Recherche d'un port disponible")
        for additive in range(1):
            is_free = await check_port(self, self.default_port + additive)
            if is_free:
                logger.info("Port libre trouvé: %r" % str(self.default_port + additive))
                self.port = self.default_port + additive
                break

        if self.port == 0:
            logger.info("Pas de port disponible trouvé ! Tentative forcée sur le port par défaut (%r) !"
                        % self.default_port)
            self.port = self.default_port

        logger.debug("Démarrage du thread serveur!")
        self.connectionThread = threading.Thread(target=self.__run_server, name=(self.__name__ + str(self.port)))
        self.connectionThread.start()

    def __run_server(self):
        """ Fonction qui démarre le serveur """
        asyncio.set_event_loop(self.loop)
        coro = self.loop.create_server(ServerProtocol, self.ip, self.port)
        logger.debug("Démarrage de la coroutine serveur! (%r, %r)" % (self.ip, self.port))
        self.server = self.loop.run_until_complete(coro)
        logger.info('Serveur démarré sur {}'.format(self.server.sockets[0].getsockname()))
        self.loop.run_forever()

    def __close(self):
        self.server.close()
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(self.server.wait_closed())
        logger.info("Le serveur a été fermé !")


class ServerProtocol(asyncio.Transport):
    def __init__(self):
        self.transport = None
    
    def connection_made(self, transport):
        self.transport = transport
        logger.info("Nouveau client à l'adresse: {}".format(transport.get_extra_info('peername')))

    def data_received(self, msg):
        logger.info("Reçu: {0} de: {1}".format(msg.decode(), self.transport.get_extra_info('peername')))

    def write(self, data):
        self.transport.write(bytes(data, encoding="utf-8"))
        logger.debug("Envoi de {0} à {1}".format(data, self.transport.get_extra_info('peername')))


    def eof_received(self):
        logger.error("OEF reçu de {}".format(self.transport.get_extra_info('peername')))

    def connection_lost(self, test):
        logger.error("Connexion perdue avec le client connecté avec {}".format(self.transport.get_extra_info('peername')))



async def check_port(cls, tested_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex((cls.ip, tested_port))
        sock.close()
        if result == 0:
            logger.debug("Résultat connexion de vérification de port favorable (%r) !" % tested_port)
            return True
        elif result == 10049:
            logger.info("L'IP définie (%r) est invalide ! Changement pour 127.0.0.1 !" % cls.ip)
            cls.ip = "127.0.0.1"
            return await check_port(cls, tested_port)
        elif result == 10061:
            logger.debug("Erreur 10061 en tentant de vérifier le port sur l'adresse %r:%r !" % (cls.ip, tested_port))
            return False
        else:
            logger.debug("connect_ex result: %r" % result)
            return False
