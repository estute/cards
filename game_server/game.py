""" components of a card game, from the perspective of the game server """

import json
import uuid
import threading


class PlayerID(object):
    """
    Representation of a player (client) in a card game.

    This is purely the the reference to a remote player used to identify
    them amongst others in the lobby or game. It does not store what cards
    they have nor control their plays.
    """

    def __init__(self, id_num, host, port):
        self.id_num = id_num
        self.host = host
        self.port = port

    @property
    def address(self):
        """
        return the address of the player client, which will be used
        to communicate with it
        """
        return "{}:{}".format(self.host, self.port)


class Lobby(object):
    """
    Representation of the 'lobby' phase of a game, in which players can join
    but gameplay has not yet begun
    """

    def __init__(self, min_players, max_players)
        self.game = game
        self.min_players = min_players
        self.max_players = max_players
        self.accepting = True
        self.players = []

    def register_player(self, player_request):
        """
        given a valid player request, create and add a player to the lobby
        if it is not already
        """
        player_request = json.loads(player_request)
        host = player_request['host']
        port = player_request['port']
        id_num = uuid.uuid4()
        player = PlayerID(id_num, host, port)
        if player not in self.players:
            self.players.append(player)
        else:
            raise PlayerConflictException()

    def _generate_status(self):
        """
        create a json status message describing the current state of the
        lobby. This will be sent out to all currently registered players
        in the lobby
        """
        return '{"accepting":"{}", "players":"{}"}'.format(
            self.accepting,
            [p.address() for p in self.players]
        )

    def is_at_quorum(self):
        """
        determine if the lobby is at `quorum`- in other words, have enough
        players registered with the lobby to begin a game
        """
        return self.min_players <= len(self.players) < self.max_players

    def serve(self, _socket):
        """
        continually serve the game lobby, accepting incoming player requests
        until the lobby has filled or timed out once quorum has been met
        """
        while True:
            pass


class PlayerConflictException(Exception):
    pass
