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

    def is_playable(self, top_card):
        if top_card.color == "WILD":
            return True
        if self.value == "Polyswin":
            return True
        return self.color == top_card.color or self.value == top_card.value

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.color == other.color and self.value == other.value
        return False

    def __hash__(self):
        return hash((self.color, self.value))

    def set_color(self, color):
        self.color = color
