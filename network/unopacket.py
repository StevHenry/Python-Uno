from game_system import player, cards
import network
import logging

logger = logging.getLogger(__name__)


class UnoPacket:
    """Forme des packets: 'PacketId#Info1-Info2-...' """

    def __init__(self):
        self.packet_id = str(packets.index(self.__class__))
        self.packet_name = self.__class__.__name__
        self.datas = []

    def get_formatted_data(self):
        return self.packet_id + "#" + "-".join(self.datas)

    def execute_server(self):
        raise NotImplementedError

    def execute_client(self):
        raise NotImplementedError

    @staticmethod
    def parse(protocol, parsed_data):
        raise NotImplementedError


class RunServerPacket(UnoPacket):
    #   Pattern: Id#True
    def __init__(self):
        UnoPacket.__init__(self)
        self.datas = (True,)

    def execute_server(self):
        pass

    def execute_client(self):
        raise NotImplementedError

    @staticmethod
    def parse(protocol, parsed_data):
        #   TODO: change parse
        return RunServerPacket()


class StopServerPacket(UnoPacket):
    #   Pattern: Id#Reason
    def __init__(self, reason):
        UnoPacket.__init__(self)
        self.reason = reason
        self.datas = (reason,)

    def execute_server(self):
        pass

    def execute_client(self):
        from network.networkmanager import client
        from graphics.window import layout_manager
        client.close_connection()
        client.ask_close = True
        layout_manager.play.error = self.reason
        layout_manager.play.display()

    @staticmethod
    def parse(protocol, parsed_data):
        return StopServerPacket(parsed_data[0])


# Same as StopServerPacket but used to refuse on player connection
class ConnectionRefusedPacket(UnoPacket):
    #   Pattern: Id#Reason
    def __init__(self, reason):
        UnoPacket.__init__(self)
        self.reason = reason
        self.datas = (reason,)

    def execute_server(self):
        pass

    def execute_client(self):
        from network.networkmanager import client
        from graphics.window import layout_manager
        client.ask_close = True
        client.close_connection()
        layout_manager.play.error = self.reason
        layout_manager.play.display()

    @staticmethod
    def parse(protocol, parsed_data):
        return ConnectionRefusedPacket(parsed_data[0])


class PlayerJoinPacket(UnoPacket):
    #   Pattern: Id#Pseudo
    def __init__(self, pl):
        UnoPacket.__init__(self)
        self.player = pl
        self.datas = (pl.pseudonym,)

    def execute_server(self):
        from game_system.game import players_in_game
        from uno_messages import messages
        for pl in network.unoserver.players:
            if pl.pseudonym == self.player.pseudonym:
                import time
                time.sleep(0.05)
                self.player.network_data.transport_protocol.send_data(ConnectionRefusedPacket(messages["error"]["pseudo_already_existing"]))
                logger.debug("Connexion d'un nouveau client refusée ! Une personne au même pseudo est déjà connectée !")
                return
        players_in_game.append(self.player.pseudonym)
        network.unoserver.add_player(self.player)
        for pl in network.unoserver.players:
            pl.network_data.transport_protocol.send_data(PlayerListPacket(players_in_game))

    def execute_client(self):
        pass

    @staticmethod
    def parse(sender_protocol, parsed_data):
        return PlayerJoinPacket(player.Player(parsed_data[0], transport_protocol=sender_protocol))


class PlayerDisconnectPacket(UnoPacket):
    #   Pattern: Id#Pseudo
    def __init__(self, pl):
        UnoPacket.__init__(self)
        self.player = pl
        self.datas = (pl.pseudonym if pl is not None else "",)

    def execute_server(self):
        from game_system.game import players_in_game
        if self.player is not None and players_in_game.__contains__(self.player.pseudonym):
            players_in_game.remove(self.player.pseudonym)
            network.unoserver.remove_player(self.player)
        for pl in network.unoserver.players:
            pl.network_data.transport_protocol.send_data(PlayerListPacket(players_in_game))

    def execute_client(self):
        pass

    @staticmethod
    def parse(sender_protocol, parsed_data):
        from network.unoserver import get_player_by_connection
        return PlayerDisconnectPacket(get_player_by_connection(sender_protocol.transport.get_extra_info('peername')[0],
                                                               sender_protocol.transport.get_extra_info('peername')[1]))


class PlayerListPacket(UnoPacket):
    #   Pattern: Id#Pseudo1-Pseudo2...
    def __init__(self, players):
        UnoPacket.__init__(self)
        self.datas = players

    def execute_server(self):
        pass

    def execute_client(self):
        from game_system.game import set_player_list
        set_player_list(self.datas)

    @staticmethod
    def parse(sender_protocol, parsed_data):
        return PlayerListPacket(parsed_data)


class PlayCardPacket(UnoPacket):
    #   Pattern: Id#Carte
    def __init__(self, card):
        UnoPacket.__init__(self)
        self.datas = (card,)

    #   TODO: Check and accept/decline
    def execute_server(self):
        pass

    #   TODO: Put card and pass to other player
    def execute_client(self):
        pass

    @staticmethod
    def parse(protocol, parsed_data):
        #   TODO: change parse
        return PlayCardPacket(parsed_data)


class RunGamePacket(UnoPacket):
    #   Pattern: Id#Carte
    def __init__(self, default_card, crds):
        UnoPacket.__init__(self)
        self.cards = crds
        self.default_card = default_card
        self.datas = []
        self.datas.append(str(default_card))
        for card_element in crds:
            self.datas.append(str(card_element))

    def execute_server(self):
        pass

    def execute_client(self):
        from graphics.GameLayout import PlayerHand, GamedPlayer, game, player_hands
        from graphics import window
        game.my_player.player_hand = self.cards
        elements = self.default_card.split("_")
        game.last_played_card = cards.NormalCard(elements[1], elements[2])
        logger.debug("First stack card: %r" % str(game.last_played_card))
        game.start_game_client()

        p_hand = PlayerHand(window.layout_manager, GamedPlayer(game.my_player, "DOWN"))
        player_hands.insert(0, p_hand)
        p_hand.show()

    @staticmethod
    def parse(protocol, parsed_data):
        crds = []
        default_card = parsed_data[0]
        parsed_data.remove(default_card)
        for element in parsed_data:
            cuts = element.split("_")
            # Pattern: "NOR" (for normal) "_" (to separate) First_color_letter "_" card number
            if cuts[0] == "NOR":
                crds.append(cards.NormalCard(cards.get_color_by_letter(cuts[1]), cuts[2]))
            # Pattern: "SPE" (for special) "_" (to separate) First_color_letter "_" card attribute
            else:
                crds.append(cards.SpecialCard(cards.get_color_by_letter(cuts[1]), cuts[2]))
        return RunGamePacket(default_card, crds)


class CardsUpdatePacket(UnoPacket):
    #   Pattern: Id#Carte
    def __init__(self, player_name, action, times):
        UnoPacket.__init__(self)
        self.player_name = player_name
        self.action = action
        self.times = times
        self.datas = (player_name, action, str(times))

    def execute_server(self):
        pass

    def execute_client(self):
        from graphics import GameLayout, window
        pl = GameLayout.get_player_hand(self.player_name)
        if pl is None:
            positions = ("RIGHT", "UP", "LEFT")
            GameLayout.player_hands.append(GameLayout.PlayerHand(
                window.layout_manager, GameLayout.GamedPlayer(player.Player(self.player_name),
                                                              positions[len(GameLayout.player_hands)-1])))
            pl = GameLayout.get_player_hand(self.player_name)
        for i in range(self.times):
            if self.action == "REMOVE":
                pl.gamed_player.player.player_hand.pop(len(pl.gamed_player.player.player_hand)-1)
            else:
                pl.gamed_player.player.player_hand.append("?CARD?")
        pl.show()

    @staticmethod
    def parse(protocol, parsed_data):
        return CardsUpdatePacket(parsed_data[0], parsed_data[1], int(parsed_data[2]))


packets = (RunServerPacket, StopServerPacket, PlayerJoinPacket, PlayerDisconnectPacket, ConnectionRefusedPacket,
           PlayerListPacket, RunGamePacket, PlayCardPacket, CardsUpdatePacket)


def parse_packet(protocol, packet_id, packet_data):
    return packets[int(packet_id)].parse(protocol, str(packet_data).split(sep="-"))

