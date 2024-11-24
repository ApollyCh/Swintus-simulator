import random


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_card(self, deck):
        card = deck.draw_card()
        self.hand.append(card)

    def play_card(self, card, top_card):
        if card.is_playable(top_card):
            self.hand.remove(card)
            return card
        return None

    def valid_actions(self, top_card):
        return [card for card in self.hand if card.is_playable(top_card)]

    def clean_hand(self):
        self.hand = []

    def __str__(self):
        return self.name
