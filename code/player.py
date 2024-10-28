import random


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.state = {}
        self.actions = {}

    def draw_card(self, deck):
        card = deck.draw_card()
        self.hand.append(card)

        self.evaluate_hand(deck)

    def evaluate_hand(self, deck):
        pass
