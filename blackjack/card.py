from __future__ import annotations
import random
from enum import Enum, unique, auto

@unique
class CardSuit(Enum):
    SPADES = auto()
    HEARTS = auto()
    DIAMONDS = auto()
    CLUBS = auto()

    @classmethod
    def get_random(cls) -> CardSuit:
        return random.choice(list(cls))

    def __str__(self) -> str:
        if not isinstance(self, CardSuit):
            raise TypeError("can only convert CardSuit to str")
        if   self is CardSuit.SPADES:   return "\\\u2660"
        elif self is CardSuit.HEARTS:   return "\\\u2665"
        elif self is CardSuit.DIAMONDS: return "\\\u2666"
        elif self is CardSuit.CLUBS:    return "\\\u2663"

@unique
class CardRank(Enum):
    ACE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
    QUEEN = auto()
    KING = auto()

    @classmethod
    def get_random(cls) -> CardRank:
        return random.choice(list(cls))

    def get_value(self) -> int:
        if   self is CardRank.ACE:   return 1
        elif self is CardRank.TWO:   return 2
        elif self is CardRank.THREE: return 3
        elif self is CardRank.FOUR:  return 4
        elif self is CardRank.FIVE:  return 5
        elif self is CardRank.SIX:   return 6
        elif self is CardRank.SEVEN: return 7
        elif self is CardRank.EIGHT: return 8
        elif self is CardRank.NINE:  return 9
        elif self is CardRank.TEN:   return 10
        elif self is CardRank.JACK:  return 10
        elif self is CardRank.QUEEN: return 10
        elif self is CardRank.KING:  return 10

    def __str__(self) -> str:
        if not isinstance(self, CardRank):
            raise TypeError("can only convert CardRank to str")
        if   self is CardRank.ACE:   return "A"
        elif self is CardRank.TWO:   return "2"
        elif self is CardRank.THREE: return "3"
        elif self is CardRank.FOUR:  return "4"
        elif self is CardRank.FIVE:  return "5"
        elif self is CardRank.SIX:   return "6"
        elif self is CardRank.SEVEN: return "7"
        elif self is CardRank.EIGHT: return "8"
        elif self is CardRank.NINE:  return "9"
        elif self is CardRank.TEN:   return "10"
        elif self is CardRank.JACK:  return "J"
        elif self is CardRank.QUEEN: return "Q"
        elif self is CardRank.KING:  return "K"

class Card:

    def __init__(self, suit: CardSuit = None, rank: CardRank = None) -> None:
        self.suit = CardSuit.get_random() if suit is None else suit
        self.rank = CardRank.get_random() if rank is None else rank

    def __repr__(self) -> str:
        return f"<Card {self.suit.name}, {self.rank.name}>"

    def __str__(self) -> str:
        return f"{self.suit}{self.rank}"