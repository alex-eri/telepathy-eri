import dbus
from telepathy._generated.Connection_Interface_Aliasing import ConnectionInterfaceAliasing
from telepathy._generated.Connection_Interface_Contact_Groups import ConnectionInterfaceContactGroups
from telepathy._generated.Connection_Interface_Contact_Info import ConnectionInterfaceContactInfo
from telepathy._generated.Connection_Interface_Contact_List import ConnectionInterfaceContactList
from telepathy._generated.Connection_Interface_Contacts import ConnectionInterfaceContacts
from utils.decorators import loggit

__author__ = 'eri'
#!/usr/bin/python

import weakref
from telepathy.server import Connection, ConnectionInterfaceRequests, Handle
import telepathy


from ..constants import PROGRAM, CLIENT_ID,CLIENT_SCOPE,CLIENT_SECRET

GROUP = 'vk.com'
from contacts import vkContacts
    # ,vkChannelInterfaceGroup
from channelmanager import vkChannelManager

from vkcom.messenger import VkMessenger, ContactList

import logging
logger = logging.getLogger('telepathy-eri/connection')

PROTOCOL = 'vk'
# many connections per manager -&gt; class for connections
# make a fancy new-type connection with a 'Requests' interface
class vkConnection(Connection,
    ConnectionInterfaceRequests,
    vkContacts,
    VkMessenger
    ):

    def __init__(self,protocol,manager, parameters):
        # self.account = parameters['account'].encode('utf-8')
        self._manager = weakref.proxy(manager)
        logger.debug('VkMessenger')
        VkMessenger.__init__(self, CLIENT_ID, CLIENT_SECRET, CLIENT_SCOPE)
        logger.debug('login')
        if parameters.get('token') and parameters['token'] != 'password':
            self.login(token=parameters['token'])
        else:
            self.login(username=parameters['account'],password=parameters['password'])

        self.alias_is_screen_name = parameters.get('alias is screen_name')
        self.contact_list = ContactList(self.Api.users,fields='nickname,screen_name,photo_50,online')

        contact = self.contact_list.get(None)

        self.account = str(contact.get('id'))

        # create a new channel manager and tell it we're it's connection
        self._channel_manager = vkChannelManager(self)

        Connection.__init__(self, PROTOCOL, self.account, PROGRAM)
        ConnectionInterfaceRequests.__init__(self)
        vkContacts.__init__(self)

        self._self_handle = self.ensure_contact_handle(contact)

        self.create_handle(telepathy.HANDLE_TYPE_LIST, 'subscribe')
        self.create_handle(telepathy.HANDLE_TYPE_LIST, 'publish')
        #     Handle(
        #     self.get_handle_id(), telepathy.HANDLE_TYPE_CONTACT,
        #     parameters['account'])
        # self._handles[telepathy.HANDLE_TYPE_CONTACT, self._self_handle.get_id()] =\
        #     self._self_handle

    # borrowed from butterfly, required by telepathy's channel init
    def handle(self, handle_type, handle_id):
        self.check_handle(handle_type, handle_id)
        return self._handles[handle_type, handle_id]

    def create_handle(self, type, name, **kwargs):
        id = self.get_handle_id()
        handle = Handle(id, type, name)
        self._handles[type, id] = handle
        return handle



    def _generate_props(self, channel_type, handle, suppress_handler, initiator_handle=None):
        props = {
            telepathy.CHANNEL_INTERFACE + '.ChannelType': channel_type,
            telepathy.CHANNEL_INTERFACE + '.TargetHandle': handle.get_id(),
            telepathy.CHANNEL_INTERFACE + '.TargetHandleType': handle.get_type(),
            telepathy.CHANNEL_INTERFACE + '.Requested': suppress_handler
            }

        if initiator_handle is not None:
            if initiator_handle.get_type() is not telepathy.HANDLE_TYPE_NONE:
                props[telepathy.CHANNEL_INTERFACE + '.InitiatorHandle'] = \
                        initiator_handle.get_id()


        return props

    def outgoing_message(self,message_id,uid,timestamp,title,text,attachments=None):
            logger.debug('out'+str((message_id,uid,timestamp,title,text,attachments)))

            handle = self.ensure_contact_handle(uid)
            props = self._generate_props(telepathy.CHANNEL_TYPE_TEXT,
                handle, False, handle)

            channel = self._channel_manager.channel_for_props(props,signal=False)
            channel.message_sent(message_id,uid,timestamp,title,text,attachments)


    def incoming_message(self,message_id,uid,timestamp,title,text,attachments=None):
            logger.debug('received'+str((message_id,uid,timestamp,title,text,attachments)))

            handle = self.ensure_contact_handle(uid)
            props = self._generate_props(telepathy.CHANNEL_TYPE_TEXT,
                handle, False, handle)

            channel = self._channel_manager.channel_for_props(props,signal=True)
            channel.message_received(message_id,uid,timestamp,title,text,attachments)




    def Connect(self):
        try:
            self.connect()
            # self.populate()
        except Exception,e:
            logger.error(e.message)
        self.StatusChanged(telepathy.CONNECTION_STATUS_CONNECTED,
            telepathy.CONNECTION_STATUS_REASON_REQUESTED)

        if self._download_at_connection:
        # if True:
            self.Download()

    def Disconnect(self):
        self.disconnect()
        self.StatusChanged(telepathy.CONNECTION_STATUS_DISCONNECTED,
            telepathy.CONNECTION_STATUS_REASON_REQUESTED)
        # stop handling all channels
        self._channel_manager.close()
        # stop handling this connection
        self._manager.disconnected(self)

    @loggit(logger)
    @dbus.service.method(telepathy.CONNECTION, in_signature='suub',
        out_signature='o', async_callbacks=('_success', '_error'))
    def RequestChannel(self, type, handle_type, handle_id, suppress_handler, _success, _error):
        self.check_connected()
        channel_manager = self._channel_manager

        if handle_id == telepathy.HANDLE_TYPE_NONE:
            handle = telepathy.server.handle.NoneHandle()
        else:
            handle = self.handle(handle_type, handle_id)
        props = self._generate_props(type, handle, suppress_handler)
        self._validate_handle(props)

        channel = channel_manager.channel_for_props(props, signal=False)

        _success(channel._object_path)
        self.signal_new_channels([channel])

