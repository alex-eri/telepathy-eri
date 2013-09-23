# telepathy-python - Base classes defining the interfaces of the Telepathy framework
#
# Copyright (C) 2005, 2006 Collabora Limited
# Copyright (C) 2005, 2006 Nokia Corporation
# Copyright (C) 2006 INdT
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
import re
import weakref

from telepathy.constants import (CONNECTION_STATUS_DISCONNECTED,
                                 CONNECTION_STATUS_CONNECTED,
                                 CONTACT_LIST_STATE_NONE,
                                 CONTACT_METADATA_STORAGE_TYPE_NONE,
                                 HANDLE_TYPE_NONE,
                                 HANDLE_TYPE_CONTACT,
                                 LAST_HANDLE_TYPE)
from telepathy.errors import (Disconnected, InvalidArgument,
                              InvalidHandle, NotAvailable,
                              NotImplemented)
from telepathy.interfaces import (CONN_INTERFACE,
                                  CONN_INTERFACE_ALIASING,
                                  CONN_INTERFACE_AVATARS,
                                  CONN_INTERFACE_CAPABILITIES,
                                  CONN_INTERFACE_PRESENCE,
                                  CONN_INTERFACE_RENAMING,
                                  CONNECTION_INTERFACE_AVATARS,
                                  CONNECTION_INTERFACE_BALANCE,
                                  CONNECTION_INTERFACE_CONTACTS,
                                  CONNECTION_INTERFACE_CONTACT_GROUPS,
                                  CONNECTION_INTERFACE_CONTACT_INFO,
                                  CONNECTION_INTERFACE_CONTACT_LIST,
                                  CONNECTION_INTERFACE_MAIL_NOTIFICATION,
                                  CONNECTION_INTERFACE_REQUESTS,
                                  CONNECTION_INTERFACE_SIMPLE_PRESENCE,
                                  CHANNEL_INTERFACE)
from telepathy.server.handle import Handle, NoneHandle
from telepathy.server.properties import DBusProperties

from telepathy._generated.Connection import Connection as _Connection

_BAD = re.compile(r'(?:^[0-9])|(?:[^A-Za-z0-9])')

def _escape_as_identifier(name):
    if isinstance(name, unicode):
        name = name.encode('utf-8')
    if not name:
        return '_'
    return _BAD.sub(lambda match: '_%02x' % ord(match.group(0)), name)

class Connection(_Connection, DBusProperties):

    _optional_parameters = {}
    _mandatory_parameters = {}
    _secret_parameters = {}
    _parameter_defaults = {}

    def __init__(self, proto, account, manager=None, protocol=None):
        """
        Parameters:
        proto - the name of the protcol this conection should be handling.
        account - a protocol-specific account name
        manager - the name of the connection manager
        """

        if manager is None:
            import warnings
            warnings.warn('The manager parameter to Connection.__init__ '
                          'should be supplied', DeprecationWarning)
            manager = 'python'

        clean_account = _escape_as_identifier(account)
        bus_name = u'org.freedesktop.Telepathy.Connection.%s.%s.%s' % \
                (manager, proto, clean_account)
        bus_name = dbus.service.BusName(bus_name, bus=dbus.SessionBus())

        object_path = '/org/freedesktop/Telepathy/Connection/%s/%s/%s' % \
                (manager, proto, clean_account)
        _Connection.__init__(self, bus_name, object_path)

        # monitor clients dying so we can release handles
        dbus.SessionBus().add_signal_receiver(self.name_owner_changed_callback,
                                              'NameOwnerChanged',
                                              'org.freedesktop.DBus',
                                              'org.freedesktop.DBus',
                                              '/org/freedesktop/DBus')

        self._interfaces = set()

        DBusProperties.__init__(self)
        self._implement_property_get(CONN_INTERFACE, {
                'SelfHandle': lambda: dbus.UInt32(self.GetSelfHandle()),
                'Interfaces': lambda: dbus.Array(self.GetInterfaces(), signature='s'),
                'Status': lambda: dbus.UInt32(self.GetStatus()),
                'HasImmortalHandles': lambda: True,
                 })

        self._proto = proto # Protocol name
        self._protocol = protocol # Protocol object

        self._status = CONNECTION_STATUS_DISCONNECTED

        self._self_handle = NoneHandle()
        self._handles = {}
        self._next_handle_id = 1
        self._client_handles = {}

        self._channels = set()
        self._next_channel_id = 0

    @property
    def self_handle(self):
        return self._self_handle

    def check_parameters(self, parameters):
        """
        Uses the values of self._mandatory_parameters and
        self._optional_parameters to validate and type check all of the
        provided parameters, and check all mandatory parameters are present.
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

    def check_connected(self):
        if self._status != CONNECTION_STATUS_CONNECTED:
            raise Disconnected('method cannot be called unless status is CONNECTION_STATUS_CONNECTED')

    def check_handle(self, handle_type, handle):
        if (handle_type, handle) not in self._handles:
            raise InvalidHandle('handle number %d not valid for type %d' %
                (handle, handle_type))

    def check_handle_type(self, type):
        if (type <= HANDLE_TYPE_NONE or type > LAST_HANDLE_TYPE):
            raise InvalidArgument('handle type %s not known' % type)

    def create_handle(self, type, name, **kwargs):
        id = self.get_handle_id()
        handle = Handle(id, type, name)
        self._handles[type, id] = handle
        return handle

    def normalize_handle_name(self, type, name):
        return name

    def ensure_handle(self, type, name, **kwargs):
        self.check_handle_type(type)
        name = self.normalize_handle_name(type, name)
        for candidate in self._handles.values():
            if candidate.type == type and candidate.name == name:
                return candidate
        return self.create_handle(type, name, **kwargs)

    def get_handle_id(self):
        id = self._next_handle_id
        self._next_handle_id += 1
        return id

    def add_client_handle(self, handle, sender):
        if sender in self._client_handles:
            self._client_handles[sender].add((handle.get_type(), handle))
        else:
            self._client_handles[sender] = set([(handle.get_type(), handle)])

    def name_owner_changed_callback(self, name, old_owner, new_owner):
        # when name and old_owner are the same, and new_owner is
        # blank, it is the client itself releasing its name... aka exiting
        if (name == old_owner and new_owner == "" and name in self._client_handles):
            print "deleting handles for", name
            del self._client_handles[name]

    def set_self_handle(self, handle):
        self._self_handle = handle

    def get_channel_path(self, suffix):
        if not suffix:
            ret = '%s/channel%d' % (self._object_path, self._next_channel_id)
            self._next_channel_id += 1
        else:
            ret = '%s/%s' % (self._object_path, suffix)
        return ret

    def add_channels(self, channels, signal=True):
        """ add new channels and signal their creation"""
        signal_channels = set()

        for channel in channels:
            if channel not in self._channels:
                self._channels.add(channel)
                signal_channels.add(channel)

        if signal:
            self.signal_new_channels(signal_channels)

    def signal_new_channels(self, channels):
        self.NewChannels([(channel._object_path,
            channel.get_immutable_properties()) for channel in channels])

        # Now NewChannel needs to be called for each new channel.
        for channel in channels:
            props = channel.get_immutable_properties()

            target_handle_type = props[CHANNEL_INTERFACE + '.TargetHandleType']
            target_handle = props[CHANNEL_INTERFACE + '.TargetHandle']
            suppress_handler = props[CHANNEL_INTERFACE + '.Requested']

            self.NewChannel(channel._object_path, channel._type,
                target_handle_type, target_handle,
                suppress_handler)

    def remove_channel(self, channel):
        if channel not in self._channels:
            return
        self._channels.remove(channel)
        self.ChannelClosed(channel._object_path)

    @dbus.service.method(CONN_INTERFACE, in_signature='', out_signature='as')
    def GetInterfaces(self):
        self.check_connected()
        return self._interfaces

    @dbus.service.method(CONN_INTERFACE, in_signature='', out_signature='s')
    def GetProtocol(self):
        return self._proto

    @dbus.service.method(CONN_INTERFACE, in_signature='uau', out_signature='as')
    def InspectHandles(self, handle_type, handles):
        self.check_connected()
        self.check_handle_type(handle_type)

        for handle in handles:
            self.check_handle(handle_type, handle)

        ret = []
        for handle in handles:
            ret.append(self._handles[handle_type, handle].get_name())

        return ret

    @dbus.service.method(CONN_INTERFACE, in_signature='uas', out_signature='au', sender_keyword='sender')
    def RequestHandles(self, handle_type, names, sender):
        self.check_connected()
        self.check_handle_type(handle_type)

        ret = []
        for name in names:
            handle = self.ensure_handle(handle_type, name)
            self.add_client_handle(handle, sender)
            ret.append(handle.get_id())

        return ret

    @dbus.service.method(CONN_INTERFACE, in_signature='uau', out_signature='', sender_keyword='sender')
    def HoldHandles(self, handle_type, handles, sender):
        pass

    @dbus.service.method(CONN_INTERFACE, in_signature='uau', out_signature='', sender_keyword='sender')
    def ReleaseHandles(self, handle_type, handles, sender):
        self.check_connected()
        self.check_handle_type(handle_type)

        for handle in handles:
            self.check_handle(handle_type, handle)
            hand = self._handles[handle_type, handle]
            if sender in self._client_handles:
                if (handle_type, hand) not in self._client_handles[sender]:
                    raise NotAvailable('client is not holding handle %s of type %s' % (handle, handle_type))
            else:
                raise NotAvailable('client does not hold any handles')

        for handle in handles:
            hand = self._handles[handle_type, handle]
            self._client_handles[sender].remove((handle_type, hand))

    @dbus.service.method(CONN_INTERFACE, in_signature='', out_signature='u')
    def GetSelfHandle(self):
        self.check_connected()
        return self._self_handle

    @dbus.service.signal(CONN_INTERFACE, signature='uu')
    def StatusChanged(self, status, reason):
        self._status = status

    @dbus.service.method(CONN_INTERFACE, in_signature='', out_signature='u')
    def GetStatus(self):
        return self._status

    @dbus.service.method(CONN_INTERFACE, in_signature='', out_signature='a(osuu)')
    def ListChannels(self):
        self.check_connected()
        ret = []
        for channel in self._channels:
            chan = (channel._object_path, channel._type, channel._handle.get_type(), channel._handle.get_id())
            ret.append(chan)
        return ret


from telepathy._generated.Connection_Interface_Aliasing \
        import ConnectionInterfaceAliasing as _ConnectionInterfaceAliasing

class ConnectionInterfaceAliasing(_ConnectionInterfaceAliasing):
    _alias_flags = 0

    def __init__(self):
        _ConnectionInterfaceAliasing.__init__(self)

    def GetAliasFlags(self):
        return dbus.UInt32(self._alias_flags)

from telepathy._generated.Connection_Interface_Avatars \
        import ConnectionInterfaceAvatars \
        as _ConnectionInterfaceAvatars

class ConnectionInterfaceAvatars(_ConnectionInterfaceAvatars, DBusProperties):

    _supported_avatar_mime_types = []
    _minimum_avatar_height = 0
    _minimum_avatar_width = 0
    _recommended_avatar_height = 0
    _recommended_avatar_width = 0
    _maximum_avatar_height = 0
    _maximum_avatar_width = 0
    _maximum_avatar_bytes = 0

    def __init__(self):
        _ConnectionInterfaceAvatars.__init__(self)

        self._implement_property_get(CONNECTION_INTERFACE_AVATARS, {
            'SupportedAvatarMIMETypes': lambda: dbus.Array(self._get_supported_avatar_mime_types(), signature='s'),
            'MinimumAvatarHeight': lambda: dbus.UInt32(self._get_minimum_avatar_height()),
            'MinimumAvatarWidth': lambda: dbus.UInt32(self._get_minimum_avatar_width()),
            'RecommendedAvatarHeight': lambda: dbus.UInt32(self._get_recommended_avatar_width()),
            'RecommendedAvatarWidth': lambda: dbus.UInt32(self._get_recommended_avatar_height()),
            'MaximumAvatarHeight': lambda: dbus.UInt32(self._get_maximum_avatar_height()),
            'MaximumAvatarWidth': lambda: dbus.UInt32(self._get_maximum_avatar_width()),
            'MaximumAvatarBytes': lambda: dbus.UInt32(self._get_maximum_avatar_bytes()),
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


from telepathy._generated.Connection_Interface_Capabilities \
        import ConnectionInterfaceCapabilities \
        as _ConnectionInterfaceCapabilities

class ConnectionInterfaceCapabilities(_ConnectionInterfaceCapabilities):
    def __init__(self):
        _ConnectionInterfaceCapabilities.__init__(self)
        # { contact handle : { str channel type : [int, int] }}
        # the first int is the generic caps, the second is the type-specific
        self._caps = {}

    @dbus.service.method(CONN_INTERFACE_CAPABILITIES, in_signature='au', out_signature='a(usuu)')
    def GetCapabilities(self, handles):
        # Usage of 0 in handles has been deprecated
        handles.remove_all(0)
        ret = []
        handle_type = HANDLE_TYPE_CONTACT
        for handle in handles:
            self.check_handle(handle_type, handle)
            if handle in self._caps:
                types = self._caps[handle]
                for ctype, specs in types.items():
                    ret.append([handle, ctype, specs[0], specs[1]])
        return ret

    @dbus.service.signal(CONN_INTERFACE_CAPABILITIES, signature='a(usuuuu)')
    def CapabilitiesChanged(self, caps):
        for handle, ctype, gen_old, gen_new, spec_old, spec_new in caps:
            self._caps.setdefault(handle, {})[ctype] = [gen_new, spec_new]

    @dbus.service.method(CONN_INTERFACE_CAPABILITIES,
                         in_signature='a(su)as', out_signature='a(su)')
    def AdvertiseCapabilities(self, add, remove):
        my_caps = self._caps.setdefault(self._self_handle, {})

        changed = {}
        for ctype, spec_caps in add:
            changed[ctype] = spec_caps
        for ctype in remove:
            changed[ctype] = None

        caps = []
        for ctype, spec_caps in changed.iteritems():
            gen_old, spec_old = my_caps.get(ctype, (0, 0))
            if spec_caps is None:
                # channel type no longer supported (provider has gone away)
                gen_new, spec_new = 0, 0
            else:
                # channel type supports new capabilities
                gen_new, spec_new = gen_old, spec_old | spec_caps
            if spec_old != spec_new or gen_old != gen_new:
                caps.append((self._self_handle, ctype, gen_old, gen_new,
                            spec_old, spec_new))

        self.CapabilitiesChanged(caps)

        # return all my capabilities
        return [(ctype, caps[1]) for ctype, caps in my_caps.iteritems()]

    def _diff_capabilities(self, handle, ctype, new_gen=None,
            new_spec=None, added_gen=None, added_spec=None):
        """Helper function to diff new caps with actual capabilities."""

        if handle in self._caps and ctype in self._caps[handle]:
            old_gen, old_spec = self._caps[handle][ctype]
        else:
            old_gen = 0
            old_spec = 0

        if new_gen is None:
            new_gen = old_gen
        if new_spec is None:
            new_spec = old_spec
        if added_gen:
            new_gen |= added_gen
        if added_spec:
            new_spec |= new_spec

        if old_gen != new_gen or old_spec != new_spec:
            diff = (int(handle), ctype, old_gen, new_gen, old_spec, new_spec)
            return diff

        return None

from telepathy._generated.Connection_Interface_Contact_Capabilities \
        import ConnectionInterfaceContactCapabilities \
        as _ConnectionInterfaceContactCapabilities

class ConnectionInterfaceContactCapabilities(_ConnectionInterfaceContactCapabilities):
    def __init__(self):
        _ConnectionInterfaceContactCapabilities.__init__(self)
        # { contact handle : list(Requestable Channel Class}
        # RCC signature is a(a{sv}as)
        self._contact_caps = {}

    def GetContactCapabilities(self, handles):
        if 0 in handles:
            raise InvalidHandle('Contact handle list contains zero')

        ret = dbus.Dictionary({}, signature='ua(a{sv}as)')
        for handle in handles:
            self.check_handle(HANDLE_TYPE_CONTACT, handle)
            caps = self._contact_caps.get(handle, [])
            ret[handle] = dbus.Array(caps, signature='(a{sv}as)')

        return ret

from telepathy._generated.Connection_Interface_Requests \
        import ConnectionInterfaceRequests \
        as _ConnectionInterfaceRequests

class ConnectionInterfaceRequests(
    _ConnectionInterfaceRequests,
    DBusProperties):

    def __init__(self):
        _ConnectionInterfaceRequests.__init__(self)
        DBusProperties.__init__(self)

        self._implement_property_get(CONNECTION_INTERFACE_REQUESTS,
            {'Channels': lambda: dbus.Array(self._get_channels(),
                signature='(oa{sv})'),
            'RequestableChannelClasses': lambda: dbus.Array(
                self._channel_manager.get_requestable_channel_classes(),
                signature='(a{sv}as)')})

    def _get_channels(self):
        return [(c._object_path, c.get_immutable_properties()) \
                for c in self._channels]

    def _check_basic_properties(self, props):
        # ChannelType must be present and must be a string.
        if CHANNEL_INTERFACE + '.ChannelType' not in props or \
                not isinstance(props[CHANNEL_INTERFACE + '.ChannelType'],
                    dbus.String):
            raise InvalidArgument('ChannelType is required')

        def check_valid_type_if_exists(prop, fun):
            p = CHANNEL_INTERFACE + '.' + prop
            if p in props and not fun(props[p]):
                raise InvalidArgument('Invalid %s' % prop)

        # Allow TargetHandleType to be missing, but not to be otherwise broken.
        check_valid_type_if_exists('TargetHandleType',
            lambda p: p >= 0 and p <= LAST_HANDLE_TYPE)

        # Allow TargetType to be missing, but not to be otherwise broken.
        check_valid_type_if_exists('TargetHandle',
            lambda p: p > 0 and p < (2**32)-1)
        if props.get(CHANNEL_INTERFACE + '.TargetHandle') == 0:
            raise InvalidArgument("TargetHandle may not be 0")

        # Allow TargetID to be missing, but not to be otherwise broken.
        check_valid_type_if_exists('TargetID',
            lambda p: isinstance(p, dbus.String))

        # Disallow InitiatorHandle, InitiatorID and Requested.
        check_valid_type_if_exists('InitiatorHandle', lambda p: False)
        check_valid_type_if_exists('InitiatorID', lambda p: False)
        check_valid_type_if_exists('Requested', lambda p: False)

        type = props[CHANNEL_INTERFACE + '.ChannelType']
        handle_type = props.get(CHANNEL_INTERFACE + '.TargetHandleType',
                HANDLE_TYPE_NONE)
        handle = props.get(CHANNEL_INTERFACE + '.TargetHandle', 0)

        return (type, handle_type, handle)

    def _validate_handle(self, props):
        target_handle_type = props.get(CHANNEL_INTERFACE + '.TargetHandleType',
            HANDLE_TYPE_NONE)
        target_handle = props.get(CHANNEL_INTERFACE + '.TargetHandle', None)
        target_id = props.get(CHANNEL_INTERFACE + '.TargetID', None)

        # Handle type 0 cannot have a handle.
        if target_handle_type == HANDLE_TYPE_NONE and target_handle not in (None, 0):
            raise InvalidArgument('When TargetHandleType is NONE, ' +
                'TargetHandle must be omitted or 0')

        # Handle type 0 cannot have a TargetID.
        if target_handle_type == HANDLE_TYPE_NONE and target_id != None:
            raise InvalidArgument('When TargetHandleType is NONE, TargetID ' +
                'must be omitted')

        if target_handle_type != HANDLE_TYPE_NONE:
            if target_handle == None and target_id == None:
                raise InvalidArgument('When TargetHandleType is not NONE, ' +
                    'either TargetHandle or TargetID must also be given')

            if target_handle != None and target_id != None:
                raise InvalidArgument('TargetHandle and TargetID must not ' +
                    'both be given')

            self.check_handle_type(target_handle_type)


    def _alter_properties(self, props):
        target_handle_type = props.get(CHANNEL_INTERFACE + '.TargetHandleType',
            HANDLE_TYPE_NONE)
        target_handle = props.get(CHANNEL_INTERFACE + '.TargetHandle', None)
        target_id = props.get(CHANNEL_INTERFACE + '.TargetID', None)

        altered_properties = props.copy()

        if target_handle_type != HANDLE_TYPE_NONE:
            if target_handle == None:
                # Turn TargetID into TargetHandle.
                for handle in self._handles.itervalues():
                    if handle.get_name() == target_id and handle.get_type() == target_handle_type:
                        target_handle = handle.get_id()
                if not target_handle:
                    raise InvalidHandle('TargetID %s not valid for type %d' % (
                        target_id, target_handle_type))

                altered_properties[CHANNEL_INTERFACE + '.TargetHandle'] = \
                    target_handle
            else:
                # Check the supplied TargetHandle is valid
                self.check_handle(target_handle_type, target_handle)

                target_id = self._handles[target_handle_type,\
                                            target_handle].get_name()
                altered_properties[CHANNEL_INTERFACE + '.TargetID'] = \
                    target_id

        altered_properties[CHANNEL_INTERFACE + '.Requested'] = True

        return altered_properties

    @dbus.service.method(CONNECTION_INTERFACE_REQUESTS,
        in_signature='a{sv}', out_signature='oa{sv}',
        async_callbacks=('_success', '_error'))
    def CreateChannel(self, request, _success, _error):
        type, handle_type, handle = self._check_basic_properties(request)
        self._validate_handle(request)
        props = self._alter_properties(request)

        channel = self._channel_manager.create_channel_for_props(props, signal=False)

        returnedProps = channel.get_immutable_properties()
        _success(channel._object_path, returnedProps)

        # CreateChannel MUST return *before* NewChannels is emitted.
        self.signal_new_channels([channel])

    @dbus.service.method(CONNECTION_INTERFACE_REQUESTS,
        in_signature='a{sv}', out_signature='boa{sv}',
        async_callbacks=('_success', '_error'))
    def EnsureChannel(self, request, _success, _error):
        type, handle_type, handle = self._check_basic_properties(request)
        self._validate_handle(request)
        props = self._alter_properties(request)

        yours = not self._channel_manager.channel_exists(props)

        channel = self._channel_manager.channel_for_props(props, signal=False)

        returnedProps = channel.get_immutable_properties()
        _success(yours, channel._object_path, returnedProps)

        self.signal_new_channels([channel])

from telepathy._generated.Connection_Interface_Mail_Notification \
        import ConnectionInterfaceMailNotification

from telepathy._generated.Connection_Interface_Presence \
        import ConnectionInterfacePresence

from telepathy._generated.Connection_Interface_Simple_Presence \
        import ConnectionInterfaceSimplePresence as _ConnectionInterfaceSimplePresence

class ConnectionInterfaceSimplePresence(_ConnectionInterfaceSimplePresence, DBusProperties):

    _statuses = {}
    _maximum_status_message_length = 0

    def __init__(self):
        _ConnectionInterfaceSimplePresence.__init__(self)
        self._implement_property_get(CONNECTION_INTERFACE_SIMPLE_PRESENCE, {
                'Statuses': lambda: dbus.Dictionary(self._get_statuses(), signature='s(ubb)'),
                'MaximumStatusMessageLength': lambda: dbus.UInt32(self._get_maximum_status_message_length()),
        })

    def _get_statuses(self):
        return self._statuses

    def _get_maximum_status_message_length(self):
        return self._maximum_status_message_length

from telepathy._generated.Connection_Interface_Contacts \
        import ConnectionInterfaceContacts as _ConnectionInterfaceContacts

class ConnectionInterfaceContacts(_ConnectionInterfaceContacts, DBusProperties):

    _contact_attribute_interfaces = {
        CONN_INTERFACE : 'contact-id',
        CONN_INTERFACE_ALIASING : 'alias',
        CONNECTION_INTERFACE_SIMPLE_PRESENCE : 'presence',
        # CONN_INTERFACE_ALIASING : 'alias',
        CONN_INTERFACE_AVATARS : 'token',
        CONNECTION_INTERFACE_CONTACT_INFO : 'info'
    }

    def __init__(self):
        _ConnectionInterfaceContacts.__init__(self)
        DBusProperties.__init__(self)

        self._implement_property_get(CONNECTION_INTERFACE_CONTACTS, {
            'ContactAttributeInterfaces': self.get_contact_attribute_interfaces,
        })

    def get_contact_attribute_interfaces(self):
        return self._contact_attribute_interfaces.keys()

    def GetContactAttributes(self, handles, interfaces, hold):
        supported_interfaces = set()
        for interface in interfaces:
            if interface in self.get_contact_attribute_interfaces():
                supported_interfaces.add(interface)

        handle_type = HANDLE_TYPE_CONTACT
        ret = dbus.Dictionary(signature='ua{sv}')
        for handle in handles:
            ret[handle] = dbus.Dictionary(signature='sv')

        functions = {
            CONN_INTERFACE: lambda x: zip(x, self.InspectHandles(handle_type, x)),
            CONNECTION_INTERFACE_SIMPLE_PRESENCE: lambda x: self.GetPresences(x).items(),
            CONN_INTERFACE_ALIASING: lambda x: self.GetAliases(x).items(),
            CONN_INTERFACE_AVATARS: lambda x: self.GetKnownAvatarTokens(x).items(),
            CONNECTION_INTERFACE_CONTACT_INFO: lambda x: self.GetContactInfo(x).items()
        }

        supported_interfaces.add(CONN_INTERFACE)

        for interface in supported_interfaces:
            interface_attribute = interface + '/' + self._contact_attribute_interfaces[interface]
            results = functions[interface](handles)
            for handle, value in results:
                ret[int(handle)][interface_attribute] = value

        return ret

from telepathy._generated.Connection_Interface_Contact_List \
        import ConnectionInterfaceContactList as _ConnectionInterfaceContactList

class ConnectionInterfaceContactList(_ConnectionInterfaceContactList, DBusProperties):

    _contact_list_state = CONTACT_LIST_STATE_NONE
    _contact_list_persists = True
    _can_change_contact_list = False
    _request_uses_message = False
    _download_at_connection = True

    def __init__(self):
        _ConnectionInterfaceContactList.__init__(self)
        DBusProperties.__init__(self)

        self._implement_property_get(CONNECTION_INTERFACE_CONTACT_LIST, {
            'ContactListState': lambda: dbus.UInt32(self._get_contact_list_state()),
            'ContactListPersists': lambda: dbus.Boolean(self._get_contact_list_persists()),
            'CanChangeContactList': lambda: dbus.Boolean(self._get_can_change_contact_list()),
            'RequestUsesMessage': lambda: dbus.Boolean(self._get_request_uses_message()),
            'DownloadAtConnection': lambda: dbus.Boolean(self._get_download_at_connection()),
        })

    @dbus.service.signal(CONNECTION_INTERFACE_CONTACT_LIST, signature='u')
    def ContactListStateChanged(self, contact_list_state):
        self._contact_list_state = contact_list_state

    def _get_contact_list_state(self):
        return self._contact_list_state

    def _get_contact_list_persists(self):
        return self._contact_list_persists

    def _get_can_change_contact_list(self):
        return self._can_change_contact_list

    def _get_request_uses_message(self):
        return self._request_uses_message

    def _get_download_at_connection(self):
        return self._download_at_connection

from telepathy._generated.Connection_Interface_Contact_Groups \
        import ConnectionInterfaceContactGroups as _ConnectionInterfaceContactGroups

class ConnectionInterfaceContactGroups(_ConnectionInterfaceContactGroups, DBusProperties):

    _disjoint_groups = False
    _group_storage = CONTACT_METADATA_STORAGE_TYPE_NONE
    _groups = []

    def __init__(self):
        _ConnectionInterfaceContactGroups.__init__(self)
        DBusProperties.__init__(self)

        self._implement_property_get(CONNECTION_INTERFACE_CONTACT_GROUPS, {
            'DisjointGroups': lambda: dbus.Boolean(self._get_disjoint_groups()),
            'GroupStorage': lambda: dbus.UInt32(self._get_group_storage()),
            'Groups': lambda: dbus.Array(self._get_groups(), signature='s'),
        })

    def _get_disjoint_groups(self):
        return self._disjoint_groups

    def _get_group_storage(self):
        return self._group_storage

    def _get_groups(self):
        return self._groups

from telepathy._generated.Connection_Interface_Contact_Info \
        import ConnectionInterfaceContactInfo as _ConnectionInterfaceContactInfo

class ConnectionInterfaceContactInfo(_ConnectionInterfaceContactInfo, DBusProperties):

    _contact_info_flags = 0
    _supported_fields = []

    def __init__(self):
        _ConnectionInterfaceContactInfo.__init__(self)
        DBusProperties.__init__(self)

        self._implement_property_get(CONNECTION_INTERFACE_CONTACT_INFO, {
            'ContactInfoFlags': lambda: dbus.UInt32(self._get_contact_info_flags()),
            'SupportedFields': lambda: dbus.Array(
                map(lambda field: dbus.Struct((field[0],dbus.Array(field[1], signature='s'), field[2], field[3]), signature='sasuu'), self._get_supported_fields()),
                signature='(sasuu)'),
        })

    def _get_contact_info_flags(self):
        return self._contact_info_flags

    def _get_supported_fields(self):
        return self._supported_fields

from telepathy._generated.Connection_Interface_Balance \
        import ConnectionInterfaceBalance as _ConnectionInterfaceBalance

class ConnectionInterfaceBalance(_ConnectionInterfaceBalance, DBusProperties):

    _account_balance = (0, 2**32-1, '')
    _manage_credit_uri = ''

    def __init__(self):
        _ConnectionInterfaceBalance.__init__(self)
        DBusProperties.__init__(self)

        self._implement_property_get(CONNECTION_INTERFACE_BALANCE, {
            'AccountBalance': lambda: dbus.Struct(self._get_account_balance(), signature='ius'),
            'ManageCreditURI': lambda: dbus.String(self._get_manage_credit_uri()),
        })

    def _get_account_balance(self):
        return self._account_balance

    def _get_manage_credit_uri(self):
        return self._manage_credit_uri
