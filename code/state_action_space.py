import pandas as pd
import numpy as np
from itertools import product


class StateActionSpace:
    """
    Each state is represented as an 18-digit identifier:
    - Digits 1-4: Number of normal cards of each color (Pink, Blue, Green, Yellow), capped at 2.
    - Digits 5-8: Number of playable normal cards of each color, capped at 2.
    - Digits 9-11: Number of each type of special card (Skip, Reverse, Draw), capped at 2.
    - Digits 12-14: Number of playable special cards of each type, capped at 2.
    - Digit 17: Presence of wild card (0 = no, 1 = yes).
    - Digit 18: Playability of wild card (0 = no, 1 = yes).
    """

    def __init__(self):
        self.state_space = []
        self.action_space = []
        self.colors = ["Pink", "Blue", "Green", "Yellow"]

    def states(self):
        """Rewrite!!! """
        values = ['0', '1', '2']

        wild_card_values = ['0', '1']

        self.state_space = [
            ''.join(state) for state in product(values, repeat=16)
            for wild in product(wild_card_values, repeat=2)
            for state in [state + wild]
        ]

        # save state_space to csv
        df = pd.DataFrame(self.state_space)
        df.to_csv('state_space.csv', index=False)

        return self.state_space


if __name__ == "__main__":
    state_action_space = StateActionSpace()
    print(state_action_space.states())
