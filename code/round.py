import random
import numpy as np
from deck import Deck
from player import Player


class Round:
    WIN_REWARD = 200
    PLAY_CARD_REWARD = 10
    SPECIAL_CARD_REWARD = 15
    DRAW_CARD_REWARD = -5
    CARD_VALUES = [0, 1, 2, 3, 4, 5, 6, 7, "Zahrapin", "Perehruck", "Khapezh", "Polyswin"]
    CARD_COLORS = ["Pink", "Blue", "Green", "Yellow", "WILD"]

    def __init__(self, deck, players):
        self.players = players
        self.deck = deck
        self.discarded = []
        self.current_player_idx = 0
        self.direction = 1
        self.to_draw = 0
        self.turn = 0
        self.top_card = None
        self.deal_cards()

    def deal_cards(self):
        for _ in range(10):
            for player in self.players:
                player.draw_card(self.deck)

        self.top_card = self.deck.draw_card()

    def reset(self):
        for player in self.players:
            player.clean_hand()

        self.deck.reset()
        self.discarded = []
        self.deal_cards()
        self.current_player_idx = 0
        self.direction = 1
        self.to_draw = 0
        self.turn = 0
        self.top_card = self.deck.draw_card()

        return self.get_state()

    def step(self, action):
        reward = 0
        player = self.players[self.current_player_idx]

        # Check if the action is to play a card
        played_card = next((card for card in player.hand if card.color == action.color and card.value == action.value),
                           None)

        # While the player cannot play a card, allow them to draw cards
        while not played_card:
            if self.deck.is_empty():
                print("Deck is empty, cannot draw.")
                break
            if len(self.deck.cards) < self.to_draw:
                self.deck.drawn_cards = self.discarded
                self.deck.resample()

            player.draw_card(self.deck)
            reward += self.DRAW_CARD_REWARD

            # Check if the drawn card is playable
            played_card = None

            for card in player.hand:
                if card.color == action.color and card.value == action.value:
                    played_card = card
                    break


        # If a playable card is found, proceed to play it
        if played_card and played_card.is_playable(self.top_card):
            player.hand.remove(played_card)
            self.discarded.append(played_card)
            self.top_card = played_card
            reward += self.PLAY_CARD_REWARD

            # Handle special cards
            if played_card.value == "Perehruck":
                self.direction *= -1
                reward += self.SPECIAL_CARD_REWARD
            elif played_card.value == "Khapezh":
                self.draw_cards_next(3)
                reward += self.SPECIAL_CARD_REWARD
            elif played_card.value == "Zahrapin":
                self.skip_next_player()
                reward += self.SPECIAL_CARD_REWARD
            elif played_card.value == "Polyswin":
                self.top_card.set_color(random.choice(self.CARD_COLORS[:-1]))
                reward += self.SPECIAL_CARD_REWARD

        done = len(player.hand) == 0
        if done:
            reward += self.WIN_REWARD

        self.advance_turn()

        return self.get_state(), reward, done

    def get_valid_actions(self):
        current_player = self.players[self.current_player_idx]
        return current_player.valid_actions(self.top_card)

    def get_state(self):
        # Fixed sizes for the top card and hand
        max_hand_size = 10  # Or whatever maximum size you expect

        top_card_color_vector = np.zeros(len(self.CARD_COLORS))
        top_card_value_vector = np.zeros(len(self.CARD_VALUES))

        if self.top_card.color in self.CARD_COLORS:
            top_card_color_vector[self.CARD_COLORS.index(self.top_card.color)] = 1
        if self.top_card.value in self.CARD_VALUES:
            top_card_value_vector[self.CARD_VALUES.index(self.top_card.value)] = 1

        # Ensure hand representation is consistent
        hand_vectors = []
        for card in self.players[self.current_player_idx].hand:
            color_vector = np.zeros(len(self.CARD_COLORS))
            value_vector = np.zeros(len(self.CARD_VALUES))

            if card.color in self.CARD_COLORS:
                color_vector[self.CARD_COLORS.index(card.color)] = 1
            if card.value in self.CARD_VALUES:
                value_vector[self.CARD_VALUES.index(card.value)] = 1

            hand_vectors.append(np.concatenate((color_vector, value_vector)))

        # Pad the hand representation if necessary
        while len(hand_vectors) < max_hand_size:
            hand_vectors.append(np.zeros(len(self.CARD_COLORS) + len(self.CARD_VALUES)))

        hand_array = np.array(hand_vectors).flatten()

        # Make sure to have consistent length for your state
        to_draw_array = np.array([self.to_draw])

        # Combine to create the state
        state = np.concatenate((top_card_color_vector, top_card_value_vector, hand_array, to_draw_array))

        return state

    def draw_cards_next(self, num_cards):
        next_player = self.players[(self.current_player_idx + self.direction) % len(self.players)]

        if len(self.deck.cards) < num_cards:
            self.deck.drawn_cards = self.discarded
            self.deck.resample()

        for _ in range(num_cards):
            next_player.draw_card(self.deck)

    def skip_next_player(self):
        self.current_player_idx = (self.current_player_idx + 2 * self.direction) % len(self.players)

    def advance_turn(self):
        self.current_player_idx = (self.current_player_idx + self.direction) % len(self.players)

    def draw_card_action(self):
        if len(self.deck.cards) == 0:
            self.deck.drawn_cards = self.discarded
            self.deck.resample()

        self.players[self.current_player_idx].draw_card(self.deck)
        self.advance_turn()
