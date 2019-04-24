from network import unoserver, unoclient
from player import Player
import asyncio
import logging

logger = logging.getLogger(__name__)


class NetworkManager:
    globals()
    server = None

    def __init__(self, is_client_connection=True, chosen_ip="0.0.0.0", chosen_port=8800):
        self.is_client = is_client_connection
        self.ip = chosen_ip
        self.port = chosen_port
        self.client = None
        self.loop = asyncio.get_event_loop()

        if is_client_connection:
            self.player = Player("pseudo", chosen_ip, chosen_port)

    async def generate(self):
        if self.is_client:
            self.client = unoclient.UnoClient(ip=self.ip, default_port=self.port)
            self.client.connect_client()
        else:
            self.server = unoserver.UnoServer(ip=self.ip, default_port=self.port)
            await self.server.create_server()

    @staticmethod
    def get_hand():
        return None

    def run(self):
        self.loop.run_until_complete(self.generate())
