
import copy
import pytest
import json

from card_lib.cards import (
    Color,
    Suit,
    Card,
    Deck,
    ImpossibleCardError,
    UnknownSuitError
)
from card_lib.ranks import CardRanksPipOnly


@pytest.fixture
def ace_high_card_rules(scope="module"):
    return CardRanksPipOnly(aces_high=True)


@pytest.fixture
def ace_low_card_rules(scope="module"):
    return CardRanksPipOnly(aces_high=False)


class TestCard(object):

    def test_card_inequality_not_card(self):
        class NotACard(object):
            def __init__(self, pip, suit):
                self.pip = pip
                self.suit = suit
        not_a_card = NotACard('K', Suit.SPADE)
        card = Card('K', Suit.SPADE)
        assert not card == not_a_card

    def test_card_inequality_different_card(self):
        card1 = Card('K', Suit.DIAMOND)
        card2 = Card('Q', Suit.DIAMOND)
        assert not card1 == card2

    def test_card_equality(self):
        card1 = Card('8', Suit.DIAMOND)
        card2 = Card('8', Suit.DIAMOND)
        assert card1 == card2

    def test_card_json_serialization(self):
        original_card = Card('9', Suit.CLUB)
        passed_card = Card.from_json(original_card.to_json())
        assert original_card == passed_card

    def test_card_json_serialization_bad_json(self):
        with pytest.raises(json.decoder.JSONDecodeError):
            Card.from_json('{')

    def test_card_json_serialization_unknown_suit(self):
        class WeirdSuit(object):
            def __init__(self, symbol):
                self.symbol = symbol
        weird_suit = WeirdSuit(u'\u2283')
        original_card = Card('9', weird_suit)
        with pytest.raises(UnknownSuitError) as ex:
            passed_card = Card.from_json(original_card.to_json())
        assert 'No suit found for symbol' in str(ex.value)


class TestCardRules(object):

    def test_beat_same_card(self, ace_high_card_rules):
        card_1 = Card('7', Suit.HEART)
        card_2 = Card('7', Suit.CLUB)
        assert ace_high_card_rules.winner(card_1, card_2) is None

    def test_beat_ace_high(self, ace_high_card_rules):
        card_1 = Card('7', Suit.HEART)
        card_2 = Card('A', Suit.CLUB)
        assert ace_high_card_rules.winner(card_1, card_2) == card_2

    def test_beat_ace_low(self, ace_low_card_rules):
        card_1 = Card('7', Suit.HEART)
        card_2 = Card('A', Suit.CLUB)
        assert ace_low_card_rules.winner(card_1, card_2) == card_1


class TestDeck(object):

    def test_add_duplicate_card(self):
        """
        make sure that trying to add a card that is already
        present within a deck throws an appropriate exception
        """
        deck = Deck()
        duplicate_card = Card('7', Suit.HEART)
        with pytest.raises(ImpossibleCardError) as ex:
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

    def test_deck_serialization(self):
        deck = Deck()
        same_deck = Deck.from_json(deck.to_json())
        assert deck._degree_of_diff(same_deck) == 0

    def test_deck_json_serialization_bad_json(self):
        with pytest.raises(json.decoder.JSONDecodeError):
            Deck.from_json('{')
