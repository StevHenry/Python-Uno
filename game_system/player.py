class Player:
    def __init__(self, player_pseudonym, transport_protocol=None):
        self.player_hand = []
        self.pseudonym = player_pseudonym
        self.network_data = NetworkData(transport_protocol=transport_protocol)

    def __str__(self):
        return self.pseudonym + "|CARDS_COUNT:" + str(len(self.player_hand)) + "|" + str(self.network_data)


class NetworkData:
    def __init__(self, transport_protocol=None):
        self.transport_protocol = transport_protocol
        if transport_protocol is not None:
            self.transport = transport_protocol.transport
            self.player_ip = str(self.transport.get_extra_info('peername')[0])
            self.player_port = int(self.transport.get_extra_info('peername')[1])

    def __str__(self):
        return "IP:" + self.player_ip + "|PORT:" + str(self.player_port)
