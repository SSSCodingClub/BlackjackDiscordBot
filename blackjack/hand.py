from __future__ import annotations
from blackjack.card import CardRank, CardSuit, Card

class Hand:

    max_hand = 21

    def __init__(self):
        self.cards: list(Card) = []

    def add_card(self, card: Card):
        self.cards.append(card)

    def is_natural(self) -> bool:
        if len(self.cards) == 2:
            contains_ace = False
            contains_ten = False
            for card in self.cards:
                if card.rank is CardRank.ACE: contains_ace = True
                elif card.rank.get_value() == CardRank.TEN.get_value(): contains_ten = True
            return contains_ace and contains_ten
        return False

    def get_optimal_value(self) -> int:
        num_aces = 0
        value = 0
        # Add all the values that are not aces
        for card in self.cards:
            if card.rank == CardRank.ACE:
                num_aces += 1
            value += card.rank.get_value()
        if num_aces > 0 and value <= 11:
            value += 10
        return value

    def is_bust(self) -> bool:
        return self.get_optimal_value() > self.max_hand

    def __str__(self) -> str:
        return str.join(" ", [str(card) for card in self.cards])