class UnoPacket:
    __name__ = "Packet"

    def __init__(self):
        self.data = None

    def get_data(self):
        return self.data


class PlayCardPacket(UnoPacket):
    def __init__(self, card):
        self.data = card


class NewPlayerConnectionPacket(UnoPacket):
    def __init__(self, player):
        self.data = player
