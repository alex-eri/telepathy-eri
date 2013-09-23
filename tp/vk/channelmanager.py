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

        _, surpress_handler, handle = self._get_type_requested_handle(props)

        if handle.get_type() == telepathy.HANDLE_TYPE_GROUP:
            path = "RosterChannel/Group/%s" % handle.get_name()
            raise telepathy.errors.NotImplemented

        elif handle.get_name() == 'subscribe' or handle.get_name() == 'publish':
            path = 'RosterChannel/List/%s' % props.get(telepathy.CHANNEL_INTERFACE + '.TargetID', )
            channel = vkContactChannel(self._conn,self,props,object_path=path)
        else:
            raise telepathy.errors.NotImplemented
        return channel


