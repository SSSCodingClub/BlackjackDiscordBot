from __future__ import annotations
from enum import Enum
from blackjack.card import CardRank, CardSuit, Card
from blackjack.dealer import Dealer
from blackjack.player import Player
import random

class BlackjackResult(Enum):
    DEALER_WIN = 0
    PLAYER_WIN = 1
    BLACKJACK = 2
    TIE = 3

class InvalidMoveException(Exception):
    pass

class Blackjack:

    def __init__(self):
        self.__deck: list(Card) = []
        for suit in CardSuit:
            for rank in CardRank:
                self.__deck.append(Card(suit, rank))
        random.shuffle(self.__deck)

        self.dealer = Dealer()
        self.player = Player()

        # When all the players have placed their bets, the dealer gives one card face up to each 
        # player in rotation clockwise, and then one card face up to themselves.
        self.dealer.hit(self.__deck)
        self.player.hit(self.__deck)

        # Another round of cards is then dealt face up to each player, but the dealer takes the 
        # second card face down. Thus, each player except the dealer receives two cards face up, and 
        # the dealer receives one card face up and one card face down.
        self.dealer.hit(self.__deck)
        self.player.hit(self.__deck)

    def hit(self) -> None:
        self.player.hit(self.__deck)

    def stand(self) -> None:
        self.player.stand()

    def play_dealer(self) -> None:
        self.dealer.play(self.__deck)

    def is_over(self) -> bool:
        return self.player.hand.is_bust() or self.player.has_stood() or self.player.hand.is_natural()

    def get_outcome(self) -> BlackjackResult:
        # Check for naturals...
        is_dealer_natural = self.dealer.hand.is_natural()
        is_player_natural = self.player.hand.is_natural()
    
        if is_player_natural: # If the player has a natural...
            if is_dealer_natural: # But the dealer also has a natural...
                return BlackjackResult.TIE # Then it's a tie!
            return BlackjackResult.BLACKJACK # Otherwise, the player wins with a blackjack!

        if is_dealer_natural: # If only the dealer has a natural...
            return BlackjackResult.DEALER_WIN # The dealer wins

        if self.player.hand.is_bust(): # If the player has bust (regardless of if the dealer bust)...
            return BlackjackResult.DEALER_WIN # The dealer wins

        if self.dealer.hand.is_bust(): # If the dealer has bust (but the player hasn't)...
            return BlackjackResult.PLAYER_WIN # The player wins

        player_value = self.player.hand.get_optimal_value()
        dealer_value = self.dealer.hand.get_optimal_value()

        if player_value > dealer_value:
            return BlackjackResult.PLAYER_WIN
        elif player_value < dealer_value:
            return BlackjackResult.DEALER_WIN
        else:
            return BlackjackResult.TIE