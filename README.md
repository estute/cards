# cards

## Description:

This repo is an experimental project, with the following purposes:

1. practice working with client, server and protocol design

2. experiment with decentralized application design

3. gain exposure to various programming languages/paradigms

There are three separate components involved:

1. card_lib - a basic python library for representing the various
   components of a card game

2. card_server* - an application that connects various players to a game
   of cards and moderates gameplay

3. card_player* - a player in the game

* name subject to change

We will continue to create new players as time goes on, implementing
them in different languages, in order to learn more about them and
see the costs and benefits that they bring when solving the same problem.

Both the card_server and card_players will exist in Docker containers. This
plus the polyglot nature of the players will require emphasis to be placed
on creating robust protocol/management design.
