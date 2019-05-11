from network import unoserver, unoclient
from network.unopacket import *
from game_system import game
import asyncio
import logging

logger = logging.getLogger(__name__)
is_host = False
server = None
client = None


def create_server(ip, port):
    global is_host, server
    is_host = True
    server = unoserver.UnoServer(ip, port)
    asyncio.get_event_loop().run_until_complete(server.create_server())


def connect_client(ip, port):
    global client
    client = unoclient.UnoClient(ip, port)
    client.connect_client()


def client_success_connect():
    global client
    client.get_client_transport().send_data(PlayerJoinPacket(game.my_player))


def launch_game():
    global client
    client.get_client_transport().send_data(RunServerPacket())
