# telepathy-python - Base classes defining the interfaces of the Telepathy framework
#
# Copyright (C) 2010 Collabora Limited
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import dbus
import dbus.service

from telepathy.constants import (CONN_MGR_PARAM_FLAG_REQUIRED,
                                 CONN_MGR_PARAM_FLAG_SECRET,
                                 CONN_MGR_PARAM_FLAG_HAS_DEFAULT)
from telepathy.errors import InvalidArgument, NotImplemented
from telepathy.interfaces import (PROTOCOL,
                                  PROTOCOL_INTERFACE_AVATARS,
                                  PROTOCOL_INTERFACE_PRESENCE)
from telepathy.server.properties import DBusProperties

from telepathy._generated.Protocol import Protocol as _Protocol

class Protocol(_Protocol, DBusProperties):

    """ Class members to override in CM implementations : """

    _english_name = ""
    _icon = ""
    _vcard_field = ""
    _authentication_types = []

    # List of Requestable_Channel_Class struct
    _requestable_channel_classes = []

    _optional_parameters = {}
    _mandatory_parameters = {}
    _secret_parameters = {}
    _parameter_defaults = {}


    def __init__(self, connection_manager, proto):
        escaped_name = proto.replace("-", "_")
        bus_name = connection_manager._name
        object_path = connection_manager._object_path + "/" + escaped_name

        _Protocol.__init__(self, bus_name, object_path)

        self._proto = proto
        self._interfaces = set()

        DBusProperties.__init__(self)
        self._implement_property_get(PROTOCOL, {
                'EnglishName': lambda: self.english_name,
                'Icon': lambda: self.icon,
                'VCardField': lambda: self.vcard_field,
                'Interfaces': lambda: self.interfaces,
                'ConnectionInterfaces': lambda: self.connection_interfaces,
                'RequestableChannelClasses': lambda: self.requestable_channels,
                'Parameters': lambda: self.parameters,
                'AuthenticationTypes': lambda: self.authentication_types,
                })

        self._add_immutable_properties({
                'EnglishName': PROTOCOL,
                'Icon': PROTOCOL,
                'VCardField': PROTOCOL,
                'Interfaces': PROTOCOL,
                'ConnectionInterfaces': PROTOCOL,
                'RequestableChannelClasses': PROTOCOL,
                'Parameters': PROTOCOL
                })

    @property
    def english_name(self):
        return dbus.String(self._english_name)

    @property
    def icon(self):
        return dbus.String(self._icon)

    @property
    def vcard_field(self):
        return dbus.String(self._vcard_field)

    @property
    def interfaces(self):
        return dbus.Array(self._interfaces, signature='s')

    @property
    def connection_interfaces(self):
        return dbus.Array(self._supported_interfaces, signature='s')

    @property
    def requestable_channels(self):
        return dbus.Array(self._requestable_channel_classes,
                signature='(a{sv}as)')

    @property
    def authentication_types(self):
        return dbus.Array(self._authentication_types, signature='s')

    @property
    def parameters(self):
        parameters = []

        secret_parameters = self._secret_parameters
        mandatory_parameters = self._mandatory_parameters
        optional_parameters = self._optional_parameters
        default_parameters = self._parameter_defaults

        for parameter_name, parameter_type in mandatory_parameters.iteritems():
            flags = CONN_MGR_PARAM_FLAG_REQUIRED
            if parameter_name in secret_parameters:
                flags |= CONN_MGR_PARAM_FLAG_SECRET
            param = (parameter_name, flags,  parameter_type, '')
            parameters.append(param)

        for parameter_name, parameter_type in optional_parameters.iteritems():
            flags = 0
            default = ''
            if parameter_name in secret_parameters:
                flags |= CONN_MGR_PARAM_FLAG_SECRET
            if parameter_name in default_parameters:
                flags |= CONN_MGR_PARAM_FLAG_HAS_DEFAULT
                default = default_parameters[parameter_name]
            param = (parameter_name, flags, parameter_type, default)
            parameters.append(param)

        return dbus.Array(parameters, signature='(susv)')

    def check_parameters(self, parameters):
        """
        Validate and type check all of the provided parameters, and
        check all mandatory parameters are present before creating a
        new connection.
        Sets defaults according to the defaults if the client has not
        provided any.
        """
        for (parm, value) in parameters.iteritems():
            if parm in self._mandatory_parameters.keys():
                sig = self._mandatory_parameters[parm]
            elif parm in self._optional_parameters.keys():
                sig = self._optional_parameters[parm]
            else:
                raise InvalidArgument('unknown parameter name %s' % parm)

            # we currently support strings, (u)int16/32 and booleans
            if sig == 's':
                if not isinstance(value, unicode):
                    raise InvalidArgument('incorrect type to %s parameter, got %s, expected a string' % (parm, type(value)))
            elif sig in 'iunq':
                if not isinstance(value, (int, long)):
                    raise InvalidArgument('incorrect type to %s parameter, got %s, expected an int' % (parm, type(value)))
            elif sig == 'b':
                if not isinstance(value, (bool, dbus.Boolean)):
                    raise InvalidArgument('incorrect type to %s parameter, got %s, expected an boolean' % (parm, type(value)))
            else:
                raise TypeError('unknown type signature %s in protocol parameters' % type)

        for (parm, value) in self._parameter_defaults.iteritems():
            if parm not in parameters:
                parameters[parm] = value

        missing = set(self._mandatory_parameters.keys()).difference(parameters.keys())
        if missing:
            raise InvalidArgument('required parameters %s not given' % missing)

    def create_connection(self, connection_manager, parameters):
        raise NotImplemented('no create_connection for %s' % self._proto)


from telepathy._generated.Protocol_Interface_Presence \
        import ProtocolInterfacePresence \
        as _ProtocolInterfacePresence

class ProtocolInterfacePresence(_ProtocolInterfacePresence):

    """ Class members to override in CM implementations : """
    _statuses = {} # Simple Status Spec Map

    def __init__(self):
        _ProtocolInterfacePresence.__init__(self)
        self._implement_property_get(PROTOCOL_INTERFACE_PRESENCE, {
                'Statuses': lambda: self.statuses})
        self._add_immutable_properties({
                'Statuses': PROTOCOL_INTERFACE_PRESENCE})

    @property
    def statuses(self):
        return dbus.Dictionary(self._statuses, signature='s(ubb)')


from telepathy._generated.Protocol_Interface_Avatars \
        import ProtocolInterfaceAvatars \
        as _ProtocolInterfaceAvatars

class ProtocolInterfaceAvatars(_ProtocolInterfaceAvatars, DBusProperties):

    _supported_avatar_mime_types = []
    _minimum_avatar_height = 0
    _minimum_avatar_width = 0
    _recommended_avatar_height = 0
    _recommended_avatar_width = 0
    _maximum_avatar_height = 0
    _maximum_avatar_width = 0
    _maximum_avatar_bytes = 0

    def __init__(self):
        _ProtocolInterfaceAvatars.__init__(self)

        self._implement_property_get(PROTOCOL_INTERFACE_AVATARS, {
            'SupportedAvatarMIMETypes': lambda: dbus.Array(self._get_supported_avatar_mime_types(), signature='s'),
            'MinimumAvatarHeight': lambda: dbus.UInt32(self._get_minimum_avatar_height()),
            'MinimumAvatarWidth': lambda: dbus.UInt32(self._get_minimum_avatar_width()),
            'RecommendedAvatarHeight': lambda: dbus.UInt32(self._get_recommended_avatar_width()),
            'RecommendedAvatarWidth': lambda: dbus.UInt32(self._get_recommended_avatar_height()),
            'MaximumAvatarHeight': lambda: dbus.UInt32(self._get_maximum_avatar_height()),
            'MaximumAvatarWidth': lambda: dbus.UInt32(self._get_maximum_avatar_width()),
            'MaximumAvatarBytes': lambda: dbus.UInt32(self._get_maximum_avatar_bytes()),
        })

        self._add_immutable_properties({
            'SupportedAvatarMIMETypes': PROTOCOL_INTERFACE_AVATARS,
            'MinimumAvatarHeight': PROTOCOL_INTERFACE_AVATARS,
            'MinimumAvatarWidth': PROTOCOL_INTERFACE_AVATARS,
            'RecommendedAvatarHeight': PROTOCOL_INTERFACE_AVATARS,
            'RecommendedAvatarWidth': PROTOCOL_INTERFACE_AVATARS,
            'MaximumAvatarHeight': PROTOCOL_INTERFACE_AVATARS,
            'MaximumAvatarWidth': PROTOCOL_INTERFACE_AVATARS,
            'MaximumAvatarBytes': PROTOCOL_INTERFACE_AVATARS,
        })

    def _get_supported_avatar_mime_types(self):
        return self._supported_avatar_mime_types

    def _get_minimum_avatar_height(self):
        return self._minimum_avatar_height

    def _get_minimum_avatar_width(self):
        return self._minimum_avatar_width

    def _get_recommended_avatar_height(self):
        return self._recommended_avatar_height

    def _get_recommended_avatar_width(self):
        return self._recommended_avatar_width

    def _get_maximum_avatar_height(self):
        return self._maximum_avatar_height

    def _get_maximum_avatar_width(self):
        return self._maximum_avatar_width

    def _get_maximum_avatar_bytes(self):
        return self._maximum_avatar_bytes
