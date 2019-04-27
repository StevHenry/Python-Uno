from game_system.player import Player


class UnoPacket:
    """Forme des packets: 'PacketId#Info1-Info2-...' """

    def __init__(self, packet_id, packet_name):
        self.packet_id = packet_id
        self.packet_name = packet_name
        self.data = None

    @staticmethod
    def parse(parsed_data):
        raise NotImplementedError


class NewPlayerPacket(UnoPacket):
    def __init__(self, player):
        UnoPacket.__init__(self, 0, NewPlayerPacket.__name__)
        #   Pattern: PacketId#Pseudo
        self.data = str(self.packet_id) + "#" + player.pseudonym

    @staticmethod
    def parse(parsed_data):
        return NewPlayerPacket(Player(parsed_data[0]))


class PlayCardPacket(UnoPacket):
    def __init__(self, card):
        UnoPacket.__init__(self, 1, PlayCardPacket.__name__)
        #   Pattern: PacketId#Carte
        self.data = str(self.packet_id) + "#" + str(card)

    @staticmethod
    def parse(parsed_data):
        #   TODO: change parse
        return PlayCardPacket(parsed_data)


__packets = (NewPlayerPacket, PlayCardPacket)


def parse_packet(packet_id, packet_data):
    return __packets[packet_id].parse(str(packet_data).split(sep="-"))
