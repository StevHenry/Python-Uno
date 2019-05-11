from game_system import cards

last_card = None


def is_normal_card_playable(card):
    global last_card
    if isinstance(card, cards.NormalCard) or card.color == card.last_card.color:
        if card.color == last_card.color or card.number == last_card.number:
            card.set_last_card(card)
            return True
    return False


def is_special_card_playable(card):
    global last_card
    if isinstance(card, cards.SpecialCard):
        if card.color == last_card.color or card.attribute == last_card.attribute or card.color == "BLACK":
            card.set_last_card(card)
            return True
    return False
