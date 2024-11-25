from __future__ import annotations

from itertools import chain
from typing import Iterable

from src.types.card import ActionCard, Card, CardColor, Effect, NumberCard


def create_deck() -> Iterable[Card]:
    """
    Create a full deck of cards for the game.

    - Includes number cards (two of each number per color).
    - Includes action cards (two of each effect per color, except POLISVIN).
    - Includes gray POLISVIN cards (eight copies total).

    Returns:
        Iterable[Card]: A full deck of cards for the game.
    """
    return chain(
        (
            NumberCard(color, value)
            for color in (
                CardColor.BLUE,
                CardColor.GREEN,
                CardColor.ORANGE,
                CardColor.PINK,
            )
            for value in range(8)
            for _ in range(2)
        ),
        (
            ActionCard(color, effect)
            for color in (
                CardColor.BLUE,
                CardColor.GREEN,
                CardColor.ORANGE,
                CardColor.PINK,
            )
            for effect in Effect
            if effect != Effect.POLISVIN
            for _ in range(2)
        ),
        (ActionCard(CardColor.GRAY, Effect.POLISVIN) for _ in range(8)),
    )
