
import copy

import pytest

from card_lib.cards import (
    Color,
    Suit,
    Card,
    Deck,
    ImpossibleCardException
)
from card_lib.ranks import CardRanksPipOnly

@pytest.fixture
def ace_high_card_rules(scope="module"):
    return CardRanksPipOnly(aces_high=True)

@pytest.fixture
def ace_low_card_rules(scope="module"):
    return CardRanksPipOnly(aces_high=False)


class TestCardRules(object):

    def test_beat_same_card(self, ace_high_card_rules):
        card_1 = Card('7', Suit.HEART)
        card_2 = Card('7', Suit.CLUB)
        assert ace_high_card_rules.beats(card_1, card_2) is None

    def test_beat_ace_high(self, ace_high_card_rules):
        card_1 = Card('7', Suit.HEART)
        card_2 = Card('A', Suit.CLUB)
        assert ace_high_card_rules.beats(card_1, card_2) == card_2

    def test_beat_ace_low(self, ace_low_card_rules):
        card_1 = Card('7', Suit.HEART)
        card_2 = Card('A', Suit.CLUB)
        assert ace_low_card_rules.beats(card_1, card_2) == card_1


class TestDeck(object):

    def test_add_duplicate_card(self):
        """
        make sure that trying to add a card that is already
        present within a deck throws an appropriate exception
        """
        deck = Deck()
        duplicate_card = Card('7', Suit.HEART)
        with pytest.raises(ImpossibleCardException) as ex:
            deck.insert(duplicate_card)
        err_msg = "Duplicate card found in deck"
        assert err_msg in str(ex.value)

    def test_degree_of_shuffle(self):
        """
        verify that the shuffling function creates a good enough randomization
        to make gameplay fun and not predictable. Since it is random,
        I consider at least 45 cards changing their initial position within
        the deck to be 'good enough'
        """
        deck = Deck()
        starting_order = copy.copy(deck)
        deck.shuffle()
        shuffled_order = deck
        assert starting_order._degree_of_diff(shuffled_order) > 45
