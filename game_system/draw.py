from game_system.cards import *
from random import shuffle

COLORS = ("GREEN", "BLUE", "RED", "YELLOW")
SPECIAL_TYPES = ("SWAP", "SKIP", "+2")
BLACK_TYPES = ("COLORSWAP", "+4")
NUMBERS = range(1, 10)


def addToDraw(newCard):
    global draw
    draw.append(newCard)


def removeFromDraw(i):
    global draw
    del(draw[i])


def getCardAtIndex(i):
    global draw
    return draw[i]


def empty():
    # efface la pioche
    global draw
    draw = []


def shuffleDraw():
    # mélange les cartes de la pioche
    global draw
    shuffle(draw)


def regenerate():
    empty()
    global draw

    for cardColor in COLORS:
        # ajoute les 0 dans la pioche
        __zeroCard = NormalCard(0, cardColor)
        addToDraw(__zeroCard)

        for k in range(2):
            for numb in NUMBERS:
                # ajoute les cartes de 1 à 9 dans la pioche
                __normalCard = NormalCard(cardColor, numb)
                addToDraw(__normalCard)

            for t in SPECIAL_TYPES:
                # ajoute les cartes spéciales de couleur dans la pioche
                __specialCard = SpecialCard(cardColor, t)
                addToDraw(__specialCard)

    for k in range(4):
        for bt in BLACK_TYPES:  # ajoute les cartes noires dans la pioche
            __blackCard = SpecialCard("BLACK", bt)
            addToDraw(__blackCard)

    shuffleDraw()


def getDrawSize():
    global draw
    return len(draw)


#initialiser la variable draw
empty()

#Debugging
regenerate()
