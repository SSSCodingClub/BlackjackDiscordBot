from __future__ import annotations
from blackjack.card import CardRank, CardSuit, Card
from blackjack.hand import Hand

class Player:

    def __init__(self) -> None:
        self.hand = Hand()
        self.__has_stood = False

    def has_stood(self) -> bool:
        return self.__has_stood

    def hit(self, deck: list(Card)) -> None:
        self.hand.add_card(deck.pop())
        if self.hand.is_natural():
            self.stand()

    def stand(self) -> None:
        self.__has_stood = True