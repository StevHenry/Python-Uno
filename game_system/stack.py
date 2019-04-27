from game_system import draw
from game_system.cards import *


__last_card = draw.getCardAtIndex(0)


def get_last_card():
    global __last_card
    return __last_card


def set_last_card(new_card):
    global __last_card
    __last_card = new_card


@staticmethod
def is_normal_card_playable(card):
    if isinstance(card, NormalCard) or card.color == __last_card.color:
        if card.color == __last_card.color or card.number == __last_card.number:
            set_last_card(card)
            return True
    return False


@staticmethod
def is_special_card_playable(card):
    if isinstance(card, SpecialCard):
        if card.color == __last_card.color or card.attribute == __last_card.attribute or card.color == "BLACK":
            set_last_card(card)
            return True
    return False

