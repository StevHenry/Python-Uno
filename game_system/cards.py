class Card:
    """Classe définissant une carte en fonction de sa couleur et
    de son numéro"""

    def __init__(self, color):
        """Construit une carte avec sa couleur"""
        self.color = color

    def __display(self):
        return str(self.color)


class NormalCard(Card):
    """Classe définissant une carte de type normal: couleur et chiffre"""
    def __init__(self, color, number):
        self.number = number
        Card.__init__(self, color)


class SpecialCard(Card):
    def __init__(self, color, attribute):
        self.attribute = attribute
        Card.__init__(self, color)
