# -*- coding: utf-8 -*-

from network.unoconnection import *
from network.unopacket import *
import threading
import asyncio
import logging
import socket

logger = logging.getLogger(__name__)
players = []


class UnoServer(UnoConnectivity):
    __name__ = "UnoServer"

    def __init__(self, default_port=8800):
        UnoConnectivity.__init__(self, default_port=default_port)
        self.loop = asyncio.new_event_loop()
        self.close_connection = self.__close
        self.local_ip = get_ip()
        self.server = None
        self.host = None

    async def create_server(self):
        """" Générer le serveur sur une intervalle de port entre 'default_port' et 'default_port'+3 """
        globals()

        logger.debug("Recherche d'un port disponible")
        for additive in range(1):
            is_free = await check_port(self, self.local_ip, self.default_port + additive)
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
        logger.info('Serveur démarré sur {0}:{1}'.format(self.local_ip, self.port))
        self.server = self.loop.run_forever()

    def __close(self, reason):
        """ Fonction qui ferme le serveur """
        for pl in players:
            pl.network_data.transport_protocol.send_data(StopServerPacket(reason))
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        self.server.close()
        new_loop.run_until_complete(self.server.wait_closed())
        self.new_loop.close()
        from game_system import game
        game.is_playing = False
        logger.info("Le serveur a été fermé !")


class ServerProtocol(asyncio.Transport):
    def __init__(self):
        self.transport = None
    
    def connection_made(self, transport):
        self.transport = transport
        logger.info("Nouveau client à l'adresse: {}".format(transport.get_extra_info("peername")))
        new_connection(transport)

    def data_received(self, data):
        logger.debug("Packet: \"{0}\" from {1}".format(data.decode(), self.transport.get_extra_info("peername")))
        packet_id, packet_data = data.decode().split("#", 1)
        parse_packet(self, packet_id, packet_data).execute_server()

    def send_data(self, packet):
        if not isinstance(packet, UnoPacket):
            raise ValueError("Specified message to send is not a UnoPacket !")
        self.transport.write(bytes(packet.get_formatted_data(), encoding="utf-8"))

    def write(self, data):
        self.transport.write(bytes(data, encoding="utf-8"))
        logger.debug("Envoi de {0} à {1}".format(data, self.transport.get_extra_info("peername")))

    def eof_received(self):
        logger.error("OEF reçu de {}".format(self.transport.get_extra_info("peername")))

    def connection_lost(self, exc):
        logger.error("Connexion perdue avec le client connecté avec %r" % str(self.transport.get_extra_info("peername")))


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


async def check_port(cls, ip, tested_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex((ip, tested_port))
        sock.close()
        if result == 0:
            logger.debug("Résultat connexion de vérification de port favorable (%r) !" % tested_port)
            return True
        elif result == 10061:
            logger.debug("Erreur 10061 en tentant de vérifier le port sur l'adresse %r:%r !" % (cls.ip, tested_port))
            return False
        else:
            logger.debug("connect_ex result: %r" % result)
            return False


def new_connection(transport):
    from game_system.game import is_playing
    from uno_messages import messages
    if len(players) >= 4:
        transport.write(bytes(ConnectionRefusedPacket(messages["error"]["server_full"]).get_formatted_data(), encoding="utf-8"))
        transport.close()
        logger.debug("Connexion d'un nouveau client refusée ! Le serveur est plein !")
        return
    elif is_playing:
        transport.write(bytes(ConnectionRefusedPacket(messages["error"]["game_started"]).get_formatted_data(), encoding="utf-8"))
        transport.close()
        logger.debug("Connexion d'un nouveau client refusée ! La partie a déjà commencé !")


def add_player(pl):
    players.append(pl)
    logger.debug("Nouveau joueur ! ({})".format(str(pl)))


def remove_player(pl):
    players.remove(pl)
    logger.debug("Joueur supprimé ! ({})".format(str(pl)))


def get_player_by_name(name):
    for pl in players:
        if pl.pseudonym == name:
            return pl
    return None


def get_player_by_connection(ip, port):
    for pl in players:
        if str(pl.network_data.player_ip) == str(ip) and int(pl.network_data.player_port) == int(port):
            return pl
    return None
