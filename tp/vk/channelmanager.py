import urllib
import time
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
    # @loggit(logger)
    def __init__(self, conn):
        self.__text_channel_id = 0
        self.__list_channel_id = 0

        ChannelManager.__init__(self, conn)
        # ChannelManager magic for handling channels
        self.implement_channel_classes(telepathy.CHANNEL_TYPE_TEXT, self._get_text_channel )

        self.implement_channel_classes(telepathy.CHANNEL_TYPE_CONTACT_LIST, self._get_list_channel )

    #def channel_for_props(self, props, signal=True, **args):
    #    channel = self.existing_channel(props)
    #    """Return an existing channel with theses properties if it already
    #    exists, otherwhise return a new one"""
    #    if channel:
    #        return channel
    #    else:
    #        chan = self.create_channel_for_props(props, signal, **args)
    #        time.sleep(1)
    #        return chan


    @loggit(logger)
    def _get_text_channel(self, props):
        # make up a name for the channel
        self.__text_channel_id += 1

        _, surpress_handler, handle = self._get_type_requested_handle(props)

        name =  handle.name or "Channel%d" % self.__text_channel_id
        path = u"Text/{}".format(name)

        return vkTextChannel(self._conn, self, props,#)
            object_path=path)


    # @loggit(logger)
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


