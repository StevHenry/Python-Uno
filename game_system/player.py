from game_system import stack, cards, draw
import logging

logger = logging.getLogger(__name__)


class Player:
    def __init__(self, player_pseudonym, player_ip=None, player_port=None):
        self.player_hand = []
        self.pseudonym = player_pseudonym
        self.player_network_data = PlayerNetworkData(player_ip, player_port)

    def init_player_hand(self):
        for k in range(7):
            self.player_hand.append(draw.getCardAtIndex(k))
            draw.removeFromDraw(k)

    def play_card(self, card_index):
        card = self.player_hand[card_index]
        if (isinstance(card, cards.NormalCard) and stack.is_normal_card_playable(card_index)) \
                or (isinstance(card, cards.SpecialCard) and stack.is_special_card_playable(card_index)):
            logger.debug("Playable card")
            del(self.player_hand[card_index])
        else:
            logger.debug("Unplayable card")

    def plus_two(self):
        for k in range(2):
                self.player_hand.append(draw.getcardAtIndex(k))
                draw.removeFromDraw(k)

    def plus_four(self):
        for k in range(2):
            self.plus_two()


class PlayerNetworkData:
    def __init__(self, player_ip, player_port):
        self.player_ip = player_ip
        self.player_port = player_port
