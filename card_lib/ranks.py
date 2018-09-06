"""
Classes to rank cards based on various card rules.
"""
from abc import ABC, abstractmethod


class CardRanksInterface(ABC):
    """
    Abstract interface to access rules around card rankings.
    """
    @abstractmethod
    def pip_score(self, card):
        """
        Score of the pip, used when calculating points at
        the end of a game. Depending on the rules of a game, aces
        can be considered high or low.

        Returns:
            score (int)
        """
        pass

    @abstractmethod
    def pip_ordinal(self, card):
        """
        Ordinal number for a given pip, which can be used
        in comparing with other pips, i.e. 10=10, J=11, etc...

        Returns:
            ordinal (int)
        """
        pass

    def winner(self, card1, card2):
        """
        Determine if card1 or card2 is ranked higher. If same rank, return None.

        Returns:
            card (Card) - highest card
        """
        if self.pip_ordinal(card1) == self.pip_ordinal(card2):
            return None
        elif self.pip_ordinal(card1) > self.pip_ordinal(card2):
            return card1
        else:
            return card2


class CardRanksPipOnly(CardRanksInterface):
    """
    Rules used by a standard card deck, based on the pip without using suit.
    Can be modified by making aces high -or- low.
    """
    def __init__(self, aces_high=True):
        self.aces_high = aces_high

    def pip_score(self, card):
        """
        the score of the pip, used when calculating points at
        the end of a game. Depending on the rules of a game, aces
        can be considered high or low.
        """
        if card.pip in ['J', 'Q', 'K']:
            return 11
        elif card.pip == 'A':
            if self.aces_high:
                return 11
            else:
                return 1
        else:
            return int(card.pip)

    def pip_ordinal(self, card):
        """
        the ordinal number for a given pip, which can be used
        in comparing with other pips, i.e. 10=10, J=11, etc...
        """
        _face_ordinals = {'J': 11, 'Q': 12, 'K': 13}
        if card.pip in ['J', 'Q', 'K']:
            return _face_ordinals[card.pip]
        if card.pip == 'A':
            if self.aces_high:
                return 14
            else:
                return 1
        else:
            return int(card.pip)
