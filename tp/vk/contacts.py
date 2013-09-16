#!/usr/bin/python
import base64
import urllib
import gobject
import time

import telepathy.errors
from tp.vk.contactlist import VkContactList
import dbus.service
import dbus
from telepathy.server import ConnectionInterfaceSimplePresence, ConnectionInterfaceContacts, ChannelTypeContactList, ChannelInterfaceGroup, ConnectionInterfaceAliasing, ConnectionInterfaceContactInfo
import telepathy
import logging
from utils.decorators import loggit

logger = logging.getLogger('Eri.Vk/contacts')
# Contacts interface with our minimal requirements implemented

GROUP = 'vk.com'
from capabilities import vkCapabilities

class vkAvatars(telepathy.server.ConnectionInterfaceAvatars):
    _supported_avatar_mime_types = ['image/jpeg', 'image/gif']
    _minimum_avatar_height = 50
    _minimum_avatar_width = 50
    _recommended_avatar_height = 100
    _recommended_avatar_width = 100
    _maximum_avatar_height = 800
    _maximum_avatar_width = 800
    _maximum_avatar_bytes = 0

    @loggit(logger)
    def RequestAvatars(self, Contacts):
        for handle_id in Contacts:
            gobject.idle_add(self.load_avatars, handle_id)

    @loggit(logger)
    def load_avatars(self, handle_id):

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
                mime = 'image/jpeg'
                if filename.split('.')[-1] == 'gif':
                    mime = 'image/gif'
                self.AvatarRetrieved(handle_id, base64.urlsafe_b64encode(url).strip('='), avatar, mime)

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


#from telepathy.server.conn import _ConnectionInterfaceContactInfo,DBusProperties,CONNECTION_INTERFACE_CONTACT_INFO

class vkInfo(ConnectionInterfaceContactInfo):

    _contact_info_flags = 1

    _supported_fields = [
        ('fn',[],telepathy.CONTACT_INFO_FIELD_FLAG_OVERWRITTEN_BY_NICKNAME,1),
        ('url',[],telepathy.CONTACT_INFO_FIELD_FLAG_OVERWRITTEN_BY_NICKNAME,2),
        ('nickname',[],telepathy.CONTACT_INFO_FIELD_FLAG_OVERWRITTEN_BY_NICKNAME,2)
    ]

    @loggit(logger)
    def GetContactInfo(self, Contacts):
        ret = dbus.Dictionary(signature='ua(sasas)')
        for handle_id in Contacts:
            info = dbus.Array(signature='(sasas)')
            handle = self.handle(telepathy.HANDLE_TYPE_CONTACT, handle_id)
            contact =  self.get_contact_info(handle.name)
            fn = dbus.Struct(('fn',[],[u'{first_name} {last_name}'.format(**contact)]),signature='sasas')
            info.append(fn)
            if 'screen_name' not in contact.keys():
                contact['screen_name']=u'id{}'.format(handle.name)
            url = dbus.Struct(('url', [], [u'http://vk.com/{screen_name}'.format(**contact)]),signature='sasas')
            info.append(url)
            if 'nickname' in contact.keys():
                nickname = dbus.Struct(('nickname', [], [u'{nickname}'.format(**contact)]),signature='sasas')
                info.append(nickname)
            else:
                logger.info(repr(contact))
            nickname = dbus.Struct(('nickname', [], [u'{screen_name}'.format(**contact)]),signature='sasas')
            info.append(nickname)
            ret[handle_id] = info
        return ret




class vkContacts(
    vkCapabilities,
    VkContactList,
    ConnectionInterfaceContacts,
    ConnectionInterfaceAliasing,
    ConnectionInterfaceSimplePresence,
    vkAvatars,
    vkInfo
):
    _contact_attribute_interfaces = {
        telepathy.CONN_INTERFACE: 'contact-id',
        telepathy.CONN_INTERFACE_ALIASING: 'alias',
        telepathy.CONNECTION_INTERFACE_SIMPLE_PRESENCE : 'presence',
        telepathy.CONN_INTERFACE_AVATARS : 'token',
        telepathy.CONNECTION_INTERFACE_CONTACT_INFO : 'info'
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
        VkContactList.__init__(self)
        vkInfo.__init__(self)
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
            if self.alias_is_screen_name:
                alias = contact.get('screen_name')
            else:
                alias = u'{first_name} {last_name}'.format(**contact)
            aliases[handle_id] = dbus.String(alias)
        return aliases

    @loggit(logger)
    def RequestAliases(self, Contacts):
        aliases = dbus.Array()
        aliases_map = self.GetAliases(Contacts)
        for handle_id in Contacts:
            aliases.append(aliases_map.get(handle_id,''))
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
                status = [2,telepathy.CONNECTION_PRESENCE_STATUS_AVAILABLE,unicode(handle.contact.get('status',u''))]
            else:
                status = [1,telepathy.CONNECTION_PRESENCE_STATUS_OFFLINE,unicode(handle.contact.get('status',u''))]

            Presences[handle.id] = dbus.Struct(status,signature='uss')

        gobject.idle_add(self.PresencesChanged,Presences)
        return Presences

    def SetPresence(self, Status, Status_Message):
        pass

    def UpdateCapabilities(self, Handler_Capabilities):
        pass