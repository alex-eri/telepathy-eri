import dbus
from connection import vkConnection

import logging
from utils.decorators import loggit

logger = logging.getLogger('Vk.Protocol')


__author__ = 'eri'
import telepathy
class vkProtocol(
    telepathy.server.Protocol,
    telepathy.server.ProtocolInterfacePresence
):

    _proto = "vk"
    # _vcard_field = ""
    _english_name = "Vk.com"
    _icon = "vk"

    _secret_parameters = [
        'password'
        'token'
    ]
    _mandatory_parameters = {
            'account' : 's',
            'password': 's'
            # 'token' : 's'
            }
    _parameter_defaults = {
            'alias is screen_name': False
    }
    _optional_parameters = {
            'alias is screen_name': 'b',
            'token':'s'
    }
    _statuses = {
        telepathy.CONNECTION_PRESENCE_STATUS_AVAILABLE: (
            telepathy.CONNECTION_PRESENCE_TYPE_AVAILABLE,
            True,
            True,
        ),
        telepathy.CONNECTION_PRESENCE_STATUS_OFFLINE: (
            telepathy.CONNECTION_PRESENCE_TYPE_OFFLINE,
            True,
            False,
        ),
    }

    _supported_interfaces = [
        telepathy.CONNECTION_INTERFACE_ALIASING,
        telepathy.CONNECTION_INTERFACE_AVATARS,
        # telepathy.CONNECTION_INTERFACE_BALANCE,
        telepathy.CONNECTION_INTERFACE_CONTACT_GROUPS,
        telepathy.CONNECTION_INTERFACE_CONTACT_INFO,
        telepathy.CONNECTION_INTERFACE_CONTACT_LIST,
        telepathy.CONNECTION_INTERFACE_CONTACTS,
        telepathy.CONNECTION_INTERFACE_REQUESTS,
        telepathy.CONNECTION_INTERFACE_SIMPLE_PRESENCE,
    ]

    _requestable_channel_classes = [
        ({   telepathy.CHANNEL + '.ChannelType': dbus.String(telepathy.CHANNEL_TYPE_TEXT),
             telepathy.CHANNEL + '.TargetHandleType': dbus.UInt32(telepathy.HANDLE_TYPE_CONTACT), },
         [   telepathy.CHANNEL + '.TargetHandle',
             telepathy.CHANNEL + '.TargetID',    ]),

        # ({telepathy.CHANNEL_INTERFACE + '.ChannelType': dbus.String(telepathy.CHANNEL_TYPE_CONTACT_LIST),
        #   telepathy.CHANNEL_INTERFACE + '.TargetHandleType': dbus.UInt32(telepathy.HANDLE_TYPE_GROUP)},
        #  [telepathy.CHANNEL_INTERFACE + '.TargetHandle',
        #   telepathy.CHANNEL_INTERFACE + '.TargetID']),

        ({telepathy.CHANNEL_INTERFACE + '.ChannelType': dbus.String(telepathy.CHANNEL_TYPE_CONTACT_LIST),
          telepathy.CHANNEL_INTERFACE + '.TargetHandleType': dbus.UInt32(telepathy.HANDLE_TYPE_LIST)},
         [telepathy.CHANNEL_INTERFACE + '.TargetHandle',
          telepathy.CHANNEL_INTERFACE + '.TargetID']),
    ]

    # @loggit(logger)
    def __init__(self, connection_manager):
        telepathy.server.Protocol.__init__(self, connection_manager, self._proto)
        telepathy.server.ProtocolInterfacePresence.__init__(self)

    @loggit(logger)
    def create_connection(self, connection_manager, parameters):
        return vkConnection(self, connection_manager, parameters)