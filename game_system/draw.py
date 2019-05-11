from game_system.cards import *
from random import shuffle

draw = []
used_draw = []


def use_card():
    """ Ajoute une carte de la pioche """
    global draw
    if len(draw) == 0:
        reload_draw()
    usable_card = get_upper_card()
    draw.remove(usable_card)
    return usable_card


def add_used_card(used_card):
    global used_draw
    used_draw.append(used_card)


def get_upper_card():
    """ Retourne la carte en haut du paquet """
    global draw
    return draw[len(draw) - 1]


def reload_draw():
    """ Ajoute toutes les cartes à la pioche """
    global draw, used_draw
    shuffle(used_draw)
    draw.extend(used_draw)
    used_draw = []


def fill_used_draw():
    for cardColor in COLORS:
        # Ajoute les 0 dans la pioche
        __zeroCard = NormalCard(cardColor, 0)
        used_draw.append(__zeroCard)

        for k in range(2):
            for numb in NUMBERS:
                # Ajoute les cartes de 1 à 9 dans la pioche
                __normalCard = NormalCard(cardColor, numb)
                used_draw.append(__normalCard)

            for special in SPECIAL_TYPES:
                # Ajoute les cartes spéciales de couleur dans la pioche
                __specialCard = SpecialCard(cardColor, special)
                used_draw.append(__specialCard)

    for k in range(4):
        for bt in BLACK_TYPES:  # Ajoute les cartes noires dans la pioche
            __blackCard = SpecialCard("BLACK", bt)
            used_draw.append(__blackCard)

