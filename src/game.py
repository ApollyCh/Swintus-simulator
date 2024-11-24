import random

import numpy as np
from deck import Deck
from player import Player
from round import Round


class Game:
    def __init__(self, num_players=2):
        self.num_players = num_players
        self.players = [Player(f"Player {i + 1}") for i in range(num_players)]
        self.deck = Deck()
        self.current_round = None

    def reset_game(self):
        self.deck.reset()
        for player in self.players:
            player.hand = []
            for _ in range(10):
                player.draw_card(self.deck)

        self.current_round = Round(self.players, self.deck)

        return self.current_round.reset()

    def start_new_round(self):
        self.current_round = Round(self.players, self.deck)
        return self.current_round.reset()

    def game_over(self):
        # The game could end based on any winning condition, like a player running out of cards
        return any(len(player.hand) == 0 for player in self.players)
