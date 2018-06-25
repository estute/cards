""" library for card games """

from enum import Enum
import random

# TODO: pick a better way to pass rules around throughout the game
ACES_HIGH = True

# The possible 'pips' or values of a given card. These include
# numbers, aces and face cards
PIPS = [
    '2', '3', '4', '5' , '6' , '7', '8', '9', '10',
    'J', 'Q', 'K', 'A'
]

class Color(Enum):
    __order__ = 'red black'
    RED = 'red'
    BLACK = 'black'

class Suit(Enum):
    __order__ = 'hearts diamonds clubs spades'
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

    @property
    def pip_score(self):
        """
        the score of the pip, used when calculating points at
        the end of a game. Depending on the rules of a game, aces
        can be considered high or low.
        """
        if self.pip in ['J', 'Q', 'K']:
            return 11
        elif self.pip == 'A':
            if ACES_HIGH:
                return 11
            else:
                return 1
        else:
            return int(self.pip)

    @property
    def pip_ordinal(self):
        """
        the ordinal number for a given pip, which can be used
        in comparing with other pips, i.e. 10=10, J=11, etc...
        """
        _face_ordinals = {'J': 11, 'Q': 12, 'K': 13}
        if self.pip in ['J', 'Q', 'K']:
            return _face_ordinals[self.pip]
        if self.pip == 'A':
            if ACES_HIGH:
                return 14
            else:
                return 1
        else:
            return int(self.pip)

    def beats(self, card):
        """
        determine if this card is ranked higher than another
        """
        return self.pip_ordinal > card.pip_ordinal


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
