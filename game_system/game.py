from game_system.player import Player
from game_system import draw, stack
from network.unopacket import RunGamePacket, CardsUpdatePacket
from tkinter import messagebox
import threading
import logging

logger = logging.getLogger(__name__)
my_player = Player("")
players_in_game = []
last_played_card = None
game_host = None
is_playing = False


def set_player_list(players):
    from graphics.window import layout_manager as lm
    from graphics import GameLayout
    global players_in_game, game_host, is_playing
    players_in_game = players
    game_host = players[0]
    rest = []

    for pl in GameLayout.player_hands:
        rest.append(pl.gamed_player.player.pseudonym)
    if is_playing:
        for x in players_in_game:
            if rest.__contains__(x):
                rest.remove(x)
        if len(rest) > 0:
            pl_hand = GameLayout.get_player_hand(rest[0])
            for cards in pl_hand.gamed_player.player.player_hand:
                draw.add_used_card(cards)
            pl_hand.grid_forget()
            GameLayout.player_hands.remove(pl_hand)
        #lm.game.display()
    else:
        lm.waiting_room.display()


def server_game_start():
    from network.unoserver import players
    from game_system.cards import SpecialCard
    draw.fill_used_draw()
    draw.reload_draw()

    stack.last_card = draw.use_card()
    while isinstance(stack.last_card, SpecialCard):
        draw.add_used_card(stack.last_card)
        stack.last_card = draw.use_card()
    draw.reload_draw()

    import time, threading
    for pl in players:
        for i in range(7):
            pl.player_hand.append(draw.use_card())
        ordered_others = players.copy()
        ordered_others.remove(pl)

        def do(sender, ordered_players):
            pl.network_data.transport_protocol.send_data(RunGamePacket(stack.last_card, pl.player_hand))
            time.sleep(1)
            for pl2 in ordered_players:
                sender.network_data.transport_protocol.send_data(CardsUpdatePacket(pl2.pseudonym, "ADD", 7))
                logger.debug("%r -> %r" % (sender.pseudonym, pl2.pseudonym))
                time.sleep(1)
        threading.Thread(target=do, args=(pl, ordered_others)).start()


def start_game_client():
    global is_playing
    is_playing = True
    logger.info("Démarrage de la partie !")
    from graphics.window import layout_manager as lm
    lm.game.display()


def ask_quit():
    def ask():
        from network import networkmanager as nm
        from uno_messages import messages
        if messagebox.askyesno(messages["quit"]["name"], messages["quit"]["question_host"] if nm.is_host else
                                                        messages["quit"]["question"], icon=messagebox.WARNING):
            from graphics.window import layout_manager
            layout_manager.play.display()
            nm.client.close_connection()
            if nm.is_host:
                nm.server.close_connection(messages["error"]["host_ended_game"])
    threading.Thread(target=ask, name="QuitThread").start()
