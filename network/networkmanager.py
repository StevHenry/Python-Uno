from network import unoserver, unoclient
from game_system.player import Player
import asyncio
import logging

logger = logging.getLogger(__name__)
server = None
client = None


def create_server():
    global server
    if server is None:
        server = unoserver.UnoServer()
        asyncio.get_event_loop().run_until_complete(server.create_server())
    else:
        server.close_connection()
        server = None
        create_server()


def connect_client():
    global client
    if client is None:
        client = unoclient.UnoClient()
        client.connect_client()
    else:
        client.close_connection()
        client = None
        connect_client()
