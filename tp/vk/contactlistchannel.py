import telepathy

__author__ = 'eri'

from tp.channel import EriChannel
from telepathy.server import ChannelTypeContactList, ChannelInterfaceGroup
import dbus
import logging
from utils.decorators import loggit

logger = logging.getLogger('Eri.Vk/list_channel')

class vkContactChannel(ChannelTypeContactList,ChannelInterfaceGroup,EriChannel):

    def __init__(self,connection,manager,props,object_path=None):

        ChannelTypeContactList.__init__(self,connection,manager,props,object_path)
        ChannelInterfaceGroup.__init__(self)
        EriChannel.__init__(self,connection,props)

        #self._object_path = object_path

    @property
    @loggit(logger)
    def _members(self):
        handles = []#dbus.Array(signature='u')
        for contact in self._conn._friends:
            handle = self._conn.ensure_contact_handle(contact)
            handles.append(int(handle))
        return handles

    @_members.setter
    def _members(self,value):
        pass


    # def GetLocalPendingMembersWithInfo(self):
    #     pass

