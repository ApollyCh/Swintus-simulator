from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

__all__ = ("CardColor", "Effect", "BaseCard", "NumberCard", "ActionCard", "Card")


class CardColor(Enum):
    BLUE = auto()
    GREEN = auto()
    ORANGE = auto()
    PINK = auto()
    GRAY = auto()  # POLISVIN


class Effect(Enum):
    KHAPYOZH = auto()
    """The next player takes 3 cards and skips a turn."""
    ZAKHRAPIN = auto()
    """The next player skips a turn."""
    POLISVIN = auto()
    """Change the current color."""
    TIKHOKHRYUN = auto()
    """Everyone must be silent, or else a penalty."""
    KHLOPKOPYT = auto()
    """Everyone puts their hand on the deck, the last one takes 2 cards."""
    PEREKHRUK = auto()
    """Changes the direction of the game."""


@dataclass
class BaseCard:
    color: CardColor
    """Card color."""


@dataclass
class NumberCard(BaseCard):
    """
    There are 64 number cards in the game set: four colors, with values from 0
    to 7, two copies of each, which allows you to intercept.
    """

    value: int
    """Card denomination. Values from 0 to 7."""


@dataclass
class ActionCard(BaseCard):
    """
    Most prescription cards come in four suits-two of each suit. All of these
    cards can be played on any card of the same color, or on another card of
    the same color of any color. The exception is the gray Poliswine card,
    which can be placed on any card. Immediately after a player plays a recipe
    card, its unique game property is triggered.
    """

    effect: Effect
    """Card effect."""


type Card = NumberCard | ActionCard
