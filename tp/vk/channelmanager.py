import urllib
import telepathy
from utils.decorators import loggit

__author__ = 'eri'
import dbus
from telepathy.server import ChannelManager

from channel import vkTextChannel
from contactlistchannel import vkContactChannel
import logging
logger = logging.getLogger('Eri.Vk/channelmanager')

# a Channel Manager with our required channels built in
class vkChannelManager(ChannelManager):
    def __init__(self, conn):
        self.__text_channel_id = 0
        self.__list_channel_id = 0

        ChannelManager.__init__(self, conn)
        # ChannelManager magic for handling channels
        self.implement_channel_classes(telepathy.CHANNEL_TYPE_TEXT, self._get_text_channel )
        self.implement_channel_classes(telepathy.CHANNEL_TYPE_CONTACT_LIST, self._get_list_channel )

    @loggit(logger)
    def _get_text_channel(self, props):
        # make up a name for the channel
        path = "TextChannel%d" % self.__text_channel_id
        self.__text_channel_id += 1
        return vkTextChannel(self._conn, self, props,#)
            object_path=path)


    @loggit(logger)
    def _get_list_channel(self,props):
        path = 'ContactList%d' % self.__list_channel_id
        self.__list_channel_id +=1
        return vkContactChannel(self._conn,self,props,object_path=path)


