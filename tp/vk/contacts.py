#!/usr/bin/python
import base64
import urllib
import gobject
import time

import telepathy.errors
from tp.vk.contactlist import VkContactList
import dbus.service
import dbus
from telepathy.server import ConnectionInterfaceSimplePresence, ConnectionInterfaceContacts, ChannelTypeContactList, ChannelInterfaceGroup, ConnectionInterfaceAliasing
import telepathy
import logging
from utils.decorators import loggit

logger = logging.getLogger('Eri.Vk/contacts')
# Contacts interface with our minimal requirements implemented

GROUP = 'vk.com'
from capabilities import vkCapabilities

class vkAvatars(telepathy.server.ConnectionInterfaceAvatars):
    _supported_avatar_mime_types = ['image/jpeg']
    _minimum_avatar_height = 50
    _minimum_avatar_width = 50
    _recommended_avatar_height = 100
    _recommended_avatar_width = 100
    _maximum_avatar_height = 800
    _maximum_avatar_width = 800
    _maximum_avatar_bytes = 0

    @loggit(logger)
    def RequestAvatars(self, Contacts):
        gobject.timeout_add(0, self.load_avatars, Contacts)

    @loggit(logger)
    def load_avatars(self, Contacts):
        for handle_id in Contacts:
            handle = self.handle(telepathy.HANDLE_TYPE_CONTACT, handle_id)
            filename = handle.contact.get('photo_cache')
            url = handle.contact.get('photo_50', '')
            if filename:
                pass
            else:
                filename, headers = urllib.urlretrieve(url)
                handle.contact['photo_cache'] = filename

            with open(filename, 'r') as f:
                avatar = dbus.ByteArray(f.read())
                self.AvatarRetrieved(handle_id, base64.urlsafe_b64encode(url).strip('='), avatar, 'image/jpeg')

    @loggit(logger)
    def GetKnownAvatarTokens(self, Contacts):
        res = dbus.Dictionary(signature='us')
        for handle_id in Contacts:
            handle = self.handle(telepathy.HANDLE_TYPE_CONTACT, handle_id)
            url = handle.contact.get('photo_50')
            if url:
                res[int(handle_id)] = base64.urlsafe_b64encode(url).strip('=')
            else:
                res[int(handle_id)] = ''

        return res

    @loggit(logger)
    def GetAvatarTokens(self,Contacts):
        return dbus.Array(self.GetKnownAvatarTokens(Contacts).values(),signature='s')


class vkContacts(
    vkCapabilities,
    VkContactList,
    ConnectionInterfaceContacts,
    ConnectionInterfaceAliasing,
    ConnectionInterfaceSimplePresence,
    vkAvatars
):
    _contact_attribute_interfaces = {
        telepathy.CONN_INTERFACE: 'contact-id',
        telepathy.CONN_INTERFACE_ALIASING: 'alias',
        telepathy.CONNECTION_INTERFACE_SIMPLE_PRESENCE : 'presence',
        telepathy.CONN_INTERFACE_AVATARS : 'token',
        # telepathy.CONNECTION_INTERFACE_CONTACT_INFO : 'info'
        # telepathy.CONNECTION_INTERFACE_CAPABILITIES : 'caps',
        # telepathy.CONNECTION_INTERFACE_CONTACT_CAPABILITIES : 'capabilities'
    }

    _statuses = {
        telepathy.CONNECTION_PRESENCE_STATUS_AVAILABLE:
            dbus.Struct((2,True,True),signature='ubb'),
        telepathy.CONNECTION_PRESENCE_STATUS_OFFLINE:
            dbus.Struct((1,True,False),signature='ubb')
    }

    _maximum_status_message_length = 160

    def __init__(self):
        logger.debug('__init__')
        ConnectionInterfaceContacts.__init__(self)
        ConnectionInterfaceAliasing.__init__(self)
        ConnectionInterfaceSimplePresence.__init__(self)
        vkCapabilities.__init__(self)
        vkAvatars.__init__(self)
        # ConnectionInterfaceContactGroups.__init__(self)
        # ConnectionInterfaceContactInfo.__init__(self)
        # ConnectionInterfaceContactList.__init__(self)

        self._implement_property_get(
            telepathy.CONNECTION_INTERFACE_CONTACTS,
            {
                'ContactAttributeInterfaces':
                    loggit(logger, 'ContactAttributeInterfaces')(
                        lambda: dbus.Array(self._contact_attribute_interfaces.keys(), signature='s')
                    )
            })


    def ensure_contact_handle(self, uid):
        """Build handle name for contact and ensure handle."""

        if type(uid) == dict:
            contact = uid
            uid = contact.get('id')

        else:
            contact = self.contact_list.get(uid)

        handle_name = str(contact.get('id',uid))

        handle = self.ensure_handle(telepathy.HANDLE_TYPE_CONTACT, handle_name)
        self._set_caps([handle])
        setattr(handle, 'contact', contact)
        return handle


    def get_contact_info(self,uid):
        return self.contact_list.get(uid)


    @loggit(logger)
    @dbus.service.method('org.freedesktop.Telepathy.Connection.Interface.Contacts', in_signature='sas',
                         out_signature='ua{sv}')
    def GetContactByID(self, Identifier, Interfaces):
        handle = self.ensure_contact_handle(Identifier)
        ret = self.GetContactAttributes([int(handle)], Interfaces, None)
        return ret[int(handle)]

    @loggit(logger)
    def GetAliases(self, Contacts):
        aliases = dbus.Dictionary(signature='us')
        for handle_id in Contacts:
            handle = self.handle(telepathy.HANDLE_TYPE_CONTACT, handle_id)
            contact =  self.get_contact_info(handle.name)
            aliases[handle_id] = dbus.String(contact.get('screen_name'))
        return aliases

    @loggit(logger)
    def RequestAliases(self, Contacts):
        aliases = dbus.Array()
        for handle_id in Contacts:
            handle = self.handle(telepathy.HANDLE_TYPE_CONTACT, handle_id)
            contact =  self.get_contact_info(handle.name)
            aliases.append(dbus.String(contact.get('screen_name')))
        return aliases

    @loggit(logger)
    @dbus.service.method('org.freedesktop.Telepathy.Connection.Interface.Aliasing', in_signature='a{us}',
                         out_signature='')
    def SetAliases(self, Aliases):
        changed = dbus.Array(signature='(us)')
        for handle_id, alias in Aliases.items():
            if handle_id == self._self_handle.get_id():
                self._self_handle.contact['screen_name'] = alias
                changed.append((handle_id, alias))
        if changed:
            self.AliasesChanged(changed)
        else:
            raise telepathy.errors.NotAvailable(repr(Aliases))

    @loggit(logger)
    def GetPresences(self, Contacts):
        Presences = dbus.Dictionary(signature='u(uss)')

        handles = {}
        names = []

        ts = time.time()

        for handle_id in Contacts:
            handle = self.handle(telepathy.HANDLE_TYPE_CONTACT, handle_id)
            handle.contact =  self.get_contact_info(handle.name)
            if handle.contact.get('status_updated', 0) < (ts - 120):
                names.append(handle.name)
            handles[handle.name]=handle
        if names:
            statuses = self.Api.users.get(user_ids=names,fields=['online','status'])
            for info in statuses:
                uid = str(info.get('id'))
                if uid in handles.keys():
                    handles[uid].contact.update(info)
                    handles[uid].contact['status_updated'] = ts


        for handle in handles.values():

            if handle.contact.get('online'):
                status = [2,telepathy.CONNECTION_PRESENCE_STATUS_AVAILABLE,handle.contact.get('status','')]
            else:
                status = [1,telepathy.CONNECTION_PRESENCE_STATUS_OFFLINE,handle.contact.get('status','')]

            Presences[handle.id] = dbus.Struct(status,signature='uss')

        gobject.idle_add(self.PresencesChanged,Presences)
        return Presences

