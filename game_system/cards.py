COLORS = ("V_GREEN", "B_BLUE", "R_RED", "J_YELLOW")
SPECIAL_TYPES = ("S", "I", "+2")
#            Switch - Interdit
BLACK_TYPES = ("COLORSWAP", "+4")
NUMBERS = range(1, 10)


class Card:
    """Classe définissant une carte en fonction de sa couleur et
    de son numéro"""

    def __init__(self, color, texture_path):
        """Construit une carte avec sa couleur"""
        self.color = color
        self.texture_path = texture_path

    def __display(self):
        return str(self.color)


class NormalCard(Card):
    """Classe définissant une carte de type normal: couleur et chiffre"""

    def __init__(self, color, number):
        self.number = number
        Card.__init__(self, color, "resources/cards/" + color[0] + str(number) + ".png")

    def __str__(self):
        return "NOR_" + self.color[0] + "_" + str(self.number)


class SpecialCard(Card):
    def __init__(self, color, attribute):
        self.attribute = attribute
        Card.__init__(self, color, "resources/cards/" + str(attribute) + ".png" if color == "BLACK" else
                      "resources/cards/" + color[0] + attribute + ".png")

    def __str__(self):
        if self.color == "BLACK":
            return "SPE_N_" + self.attribute
        return "SPE_" + self.color[0] + "_" + str(self.attribute)


def get_color_by_letter(letter):
    for color in COLORS:
        if color[0] == letter:
            return color
    if letter == "N":
        return "BLACK"
    return None
