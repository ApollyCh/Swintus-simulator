class Card:
    """
    Card class for the game. Each card has a color and a value.
    Colors: [Pink, Blue, Green, Yellow, "WILD"]
    Values: [0, 1, 2, 3, 4, 5, 6, 7, "Zahrapin", "Perehruck", "Khapezh", "Polyswin"]
    """

    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return f"{self.color} {self.value}"

    def evaluate_card(self, top_card):
        """
        Evaluates if the card can be placed on the top card.
        :param top_card: Card object
        :return: True if the card can be placed, False otherwise
        """
        if self.color == top_card.color or self.value == top_card.value:
            return True
        return False
