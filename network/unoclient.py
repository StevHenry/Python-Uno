# -*- coding: utf-8 -*-

from network.unoconnection import *
from network.unopacket import *
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
            self.loop.run_forever()
        except ConnectionRefusedError as e:
            self.connection_error = e
            logger.debug("Client connection to provided server is impossible !")

    def __close(self):
        from game_system.game import my_player
        self.client.send_data(PlayerDisconnectPacket(my_player))
        if self.is_linked:
            self.client.disconnect()
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

    def disconnect(self):
        self.transport.close()
        self.uno_client.set_connected(False)

    def connection_made(self, transport):
        self.transport = transport
        self.uno_client.set_connected(True)

    def data_received(self, data):
        logger.debug("Packet: \"{}\" from SERVER".format(data.decode()))
        packet_id, packet_data = data.decode().split("#", 1)
        parse_packet(self, packet_id, packet_data).execute_client()

    def send_data(self, packet):
        if not isinstance(packet, UnoPacket):
            raise ValueError("Specified messages to send is not a UnoPacket !")
        self.transport.write(bytes(packet.get_formatted_data(), encoding="utf-8"))

    def connection_lost(self, exc):
        logger.warning("Connexion perdue ! ({})".format(str(exc)))
        from graphics.window import layout_manager
        from uno_messages import messages
        if layout_manager.play.error is None:
            layout_manager.play.error = messages["error"]["connection_lost"]
        self.uno_client.set_connected(False)
        self.loop.stop()
