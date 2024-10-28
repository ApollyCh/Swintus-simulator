import random
from card import Card


class Deck:
    """A deck of cards.
        Each deck has 94 cards. 64 of them are normal cards, 30 are special cards.
    """

    def __init__(self):
        self.cards = []
        self.drawn_cards = []
        self.create_deck()
        self.shuffle_deck()

    def create_deck(self):
        colors = ["Pink", "Blue", "Green", "Yellow"]
        values = [0, 1, 2, 3, 4, 5, 6, 7, "Zahrapin", "Perehruck", "Khapezh"]

        number_cards = [Card(color, value) for color in colors for value in values] * 2
        poly_card = [Card("WILD", "Polyswin")] * 6

        self.cards = number_cards + poly_card

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) == 0:
            self.cards = self.drawn_cards
            self.drawn_cards = []

        return self.cards.pop()

    def discard_card(self, card):
        self.drawn_cards.append(card)
