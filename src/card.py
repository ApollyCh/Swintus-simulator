# @see https://github.com/datamllab/rlcard/blob/master/rlcard/games/uno/card.py

from termcolor import colored


class Card:
    info = {
        "type": ["number", "action", "wild"],
        "color": ["r", "g", "b", "y"],
        "trait": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "skip",
            "reverse",
            "draw_3",
            "wild",
        ],
    }

    def __init__(self, card_type, color, trait):
        """Initialize the class of Card

        Args:
            card_type (str): The type of card
            color (str): The color of card
            trait (str): The trait of card
        """
        self.type = card_type
        self.color = color
        self.trait = trait
        self.str = self.get_str()

    def get_str(self):
        """Get the string representation of card

        Return:
            (str): The string of card's color and trait
        """
        return self.color + "-" + self.trait

    @staticmethod
    def print_cards(cards, wild_color=False):
        """Print out card in a nice form

        Args:
            card (str or list): The string form or a list of a card
            wild_color (boolean): True if assign collor to wild cards
        """
        if isinstance(cards, str):
            cards = [cards]
        for i, card in enumerate(cards):
            if card == "draw":
                trait = "Draw"
            else:
                color, trait = card.split("-")
                if trait == "skip":
                    trait = "Skip"
                elif trait == "reverse":
                    trait = "Reverse"
                elif trait == "draw_3":
                    trait = "Draw-3"
                elif trait == "wild":
                    trait = "Wild"

            if trait == "Draw" or (trait[:4] == "Wild" and not wild_color):
                print(trait, end="")
            elif color == "r":  # type: ignore
                print(colored(trait, "red"), end="")
            elif color == "g":  # type: ignore
                print(colored(trait, "green"), end="")
            elif color == "b":  # type: ignore
                print(colored(trait, "blue"), end="")
            elif color == "y":  # type: ignore
                print(colored(trait, "yellow"), end="")

            if i < len(cards) - 1:
                print(", ", end="")
