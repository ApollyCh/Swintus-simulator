# @see https://github.com/datamllab/rlcard/blob/master/rlcard/games/uno/utils.py

from collections import OrderedDict

import numpy as np

from .card import Card

ACTION_SPACE = OrderedDict(
    {
        "r-0": 0,
        "r-1": 1,
        "r-2": 2,
        "r-3": 3,
        "r-4": 4,
        "r-5": 5,
        "r-6": 6,
        "r-7": 7,
        "r-skip": 8,
        "r-reverse": 9,
        "r-draw_3": 10,
        "r-wild": 11,
        "g-0": 12,
        "g-1": 13,
        "g-2": 14,
        "g-3": 15,
        "g-4": 16,
        "g-5": 17,
        "g-6": 18,
        "g-7": 19,
        "g-skip": 20,
        "g-reverse": 21,
        "g-draw_3": 22,
        "g-wild": 23,
        "b-0": 24,
        "b-1": 25,
        "b-2": 26,
        "b-3": 27,
        "b-4": 28,
        "b-5": 29,
        "b-6": 30,
        "b-7": 31,
        "b-skip": 32,
        "b-reverse": 33,
        "b-draw_3": 34,
        "b-wild": 35,
        "y-0": 36,
        "y-1": 37,
        "y-2": 38,
        "y-3": 39,
        "y-4": 40,
        "y-5": 41,
        "y-6": 42,
        "y-7": 43,
        "y-skip": 44,
        "y-reverse": 45,
        "y-draw_3": 46,
        "y-wild": 47,
        "draw": 48,
    }
)
ACTION_LIST = list(ACTION_SPACE.keys())

# a map of color to its index
COLOR_MAP = {"r": 0, "g": 1, "b": 2, "y": 3}

# a map of trait to its index
TRAIT_MAP = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "skip": 8,
    "reverse": 9,
    "draw_3": 10,
    "wild": 11,
}

WILD = ["r-wild", "g-wild", "b-wild", "y-wild"]


def init_deck():
    """Generate swintus deck"""
    deck = []
    card_info = Card.info
    for color in card_info["color"]:
        # init number cards
        for num in card_info["trait"][:8]:
            deck.append(Card("number", color, num))
            deck.append(Card("number", color, num))

        # init action cards
        for action in card_info["trait"][8:11]:
            deck.append(Card("action", color, action))
            deck.append(Card("action", color, action))

        # init wild cards
        deck.append(Card("wild", color, card_info["trait"][11]))
        deck.append(Card("wild", color, card_info["trait"][11]))
    return deck


def cards2list(cards):
    """Get the corresponding string representation of cards

    Args:
        cards (list): list of UnoCards objects

    Returns:
        (string): string representation of cards
    """
    cards_list = []
    for card in cards:
        cards_list.append(card.get_str())
    return cards_list


def hand2dict(hand):
    """Get the corresponding dict representation of hand

    Args:
        hand (list): list of string of hand's card

    Returns:
        (dict): dict of hand
    """
    hand_dict = {}
    for card in hand:
        if card not in hand_dict:
            hand_dict[card] = 1
        else:
            hand_dict[card] += 1
    return hand_dict


def encode_hand(plane, hand):
    """Encode hand and represerve it into plane

    Args:
        plane (array): 3*4*12 numpy array
        hand (list): list of string of hand's card

    Returns:
        (array): 3*4*12 numpy array
    """
    # plane = np.zeros((3, 4, 12), dtype=int)
    plane[0] = np.ones((4, 12), dtype=int)
    hand = hand2dict(hand)
    for card, count in hand.items():
        card_info = card.split("-")
        color = COLOR_MAP[card_info[0]]
        trait = TRAIT_MAP[card_info[1]]
        if trait >= 11:
            if plane[1][0][trait] == 0:
                for index in range(4):
                    plane[0][index][trait] = 0
                    plane[1][index][trait] = 1
        else:
            plane[0][color][trait] = 0
            plane[count][color][trait] = 1
    return plane


def encode_target(plane, target):
    """Encode target and represerve it into plane

    Args:
        plane (array): 1*4*12 numpy array
        target(str): string of target card

    Returns:
        (array): 1*4*12 numpy array
    """
    target_info = target.split("-")
    color = COLOR_MAP[target_info[0]]
    trait = TRAIT_MAP[target_info[1]]
    plane[color][trait] = 1
    return plane
