from game_system.player import Player
from game_system import draw, stack
from network.unopacket import RunGamePacket
import logging

logger = logging.getLogger(__name__)
my_player = Player("")
players_in_game = []
last_played_card = None
game_host = None


def set_player_list(players):
    from graphics.window import layout_manager as lm
    global players_in_game, game_host
    players_in_game = players
    game_host = players[0]
    lm.waiting_room.display()


def server_game_start():
    from network.unoserver import players
    draw.fill_used_draw()
    draw.reload_draw()

    stack.last_card = draw.use_card()

    for pl in players:
        for i in range(7):
            pl.player_hand.append(draw.use_card())
        pl.network_data.transport_protocol.send_data(RunGamePacket(stack.last_card, pl.player_hand))


def start_game_client():
    from graphics.window import layout_manager as lm

    lm.game.display()
