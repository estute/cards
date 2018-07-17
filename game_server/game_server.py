
import socket
import sys
import json
import logging

from game import (
    PlayerID,
    PlayerConflictException
    Lobby
)

logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def create_socket(host, port):
    """
    create a socket object and bind it to a port. This will
    be used to communicate between the various players within
    a game
    """
    LOG.debug('Creating a socket and binding to {} on {}'.format(
        host, port
    ))
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        _socket.bind((host, port))
    except socket.error:
        error_msg = 'Unable to bind socket to {} on {}'.format(
            host, port
        )
        LOG.error(error_msg)
        sys.exit(1)
    LOG.debug('Successfully bound socket')
    return _socket

def handle_player_request(connection):

def main():
    # for now, using hard coded values
    _socket = create_socket('localhost', 8080)
    lobby = Lobby('go fish', 2, 5)
    lobby.serve(_socket)

if __name__ == "__main__":
    main()
