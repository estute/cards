"""
Classes for defining cards, card characteristics, and card decks.
"""

from enum import Enum
import random

# The possible 'pips' or values of a given card. These include
# numbers, aces and face cards
PIPS = [
    '2', '3', '4', '5' , '6' , '7', '8', '9', '10',
    'J', 'Q', 'K', 'A'
]

class Color(Enum):
    __order__ = 'RED BLACK'
    RED = 'red'
    BLACK = 'black'


class Suit(Enum):
    __order__ = 'HEART DIAMOND CLUB SPADE'
    HEART = ('hearts', u'\u2665', Color.RED)
    DIAMOND = ('diamonds', u'\u2666', Color.RED)
    CLUB = ('clubs', u'\u2663', Color.BLACK)
    SPADE = ('spades', u'\u2660', Color.BLACK)

    def __init__(self, suit_name, symbol, color):
        self.suit_name = suit_name
        self.symbol = symbol
        self.color = color

    def __str__(self):
        return self.symbol


class Card(object):

    def __init__(self, pip, suit):
        self.pip = pip
        self.suit = suit

    def __str__(self):
        return '{} {}'.format(self.pip, self.suit)

    def __eq__(self, other):
        return self.pip == other.pip and self.suit == other.suit


class Deck(object):
    """
    A deck of cards used in a game. The deck is represented as a
    LIFO list, with the top of the deck (first card to deal) is
    the last card in the list.
    """

    def __init__(self, full_deck=True):
        if full_deck:
            self.cards = [
                Card(pip, suit) for pip in PIPS for suit in Suit
            ]
        else:
            self.cards = []

    def __str__(self):
        return ','.join([str(c) for c in self.cards])

    @property
    def size(self):
        return len(self.cards)

    def _split(self, position):
        """
        helper function for splitting the deck into two smaller decks,
        at a specified postion
        """
        return self.cards[0:position], self.cards[position:]

    def _swap(self, pos_1, pos_2):
        """
        helper function for swapping the position of two cards
        within the deck
        """
        card_1 = self.cards[pos_1]
        card_2 = self.cards[pos_2]
        self.cards[pos_1] = card_2
        self.cards[pos_2] = card_1

    def insert(self, card, position=0):
        """
        insert a card at a given position in the deck. This defaults
        to inserting them at the bottom of the deck
        """
        if card in self.cards:
            raise ImpossibleCardException(
                "Duplicate card found in deck"
            )
        first_chunk, second_chunk = self._split(position)
        new_deck = first_chunk
        new_deck.append(card)
        new_deck.extend(second_chunk)
        self.cards = new_deck

    def deal(self, position=None):
        """
        deal a card from the deck, from a specified position. Defaults
        to dealing from the top of the deck.
        """
        if position:
            return self.cards.pop(position)
        else:
            return self.cards.pop()

    def shuffle(self):
        """
        shuffle the order of the cards in the deck.
        """
        for step in range(self.size):
            card = self.cards.pop()
            new_pos = random.randint(0, self.size - 1)
            self.insert(card, new_pos)

    def _degree_of_diff(self, other_deck):
        """
        helper function for calculating how shuffled a deck of cards is compared
        to another.
        * The `other deck` represents the this deck, but prior to the shuffle
        * The degree of shuffling is decided by comparing how many cards have
        moved from their initial position
        """
        return list(map(
            lambda pair: pair[0] == pair[1], zip(self.cards, other_deck.cards)
        )).count(False)


class ImpossibleCardException(Exception):
    pass
