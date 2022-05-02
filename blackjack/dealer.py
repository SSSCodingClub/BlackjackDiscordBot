from __future__ import annotations
from blackjack.card import CardRank, CardSuit, Card
from blackjack.hand import Hand

class Dealer:

    def __init__(self) -> None:
        self.hand = Hand()

    def hit(self, deck: list(Card)) -> None:
        self.hand.add_card(deck.pop())

    def play(self, deck: list(Card)) -> None:
        while self.hand.get_optimal_value() < 17:
            self.hit(deck)
        