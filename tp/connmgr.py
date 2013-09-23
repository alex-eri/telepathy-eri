from utils.decorators import loggit
from vk.protocol import vkProtocol

__author__ = 'eri'
import logging
logger = logging.getLogger('Eri.ConnectionManager')


# create a telepathy ConnectionManager for 'cave'
from telepathy.server import ConnectionManager

from constants import PROTOCOL, PROGRAM
from vk.connection import vkConnection

class eriConnectionManager(ConnectionManager):
    # @loggit(logger)
    def __init__(self):
        ConnectionManager.__init__(self, PROGRAM)
        # use telepathy magic to provide required methods
        logger.debug('init')
        self._implement_protocol('vk',vkProtocol)

    def quit(self):
        "Terminates all connections. Must be called upon quit"
        conns = self._connections.copy()
        for connection in conns:
            connection.Disconnect()
        logger.info("Connection manager quitting")