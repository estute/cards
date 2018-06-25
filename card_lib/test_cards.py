
import unittest
import copy

import pytest

from card_lib.cards import (
    Color,
    Suit,
    Card,
    Deck,
    ImpossibleCardException
)

class TestCards(unittest.TestCase):

    def test_beat_same_card(self):
        card_1 = Card('7', Suit.HEART)
        card_2 = Card('7', Suit.CLUB)
        self.assertFalse(card_1.beats(card_2))

    def test_beat_ace_high(self):
        card_1 = Card('7', Suit.HEART)
        card_2 = Card('A', Suit.CLUB)
        self.assertFalse(card_1.beats(card_2))


class TestDeck(unittest.TestCase):

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
        self.assertTrue(err_msg in str(ex.value))

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
        self.assertTrue(starting_order._degree_of_diff(shuffled_order) > 45)
