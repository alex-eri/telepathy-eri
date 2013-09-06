# -*- coding: utf-8 -*-
# Generated from the Telepathy spec
"""Copyright © 2009–2011 Collabora Ltd.
Copyright © 2009 Nokia Corporation

    This library is free software; you can redistribute it and/or
      modify it under the terms of the GNU Lesser General Public
      License as published by the Free Software Foundation; either
      version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
      but WITHOUT ANY WARRANTY; without even the implied warranty of
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
      Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
      License along with this library; if not, write to the Free Software
      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
      USA.
  
"""

import dbus.service


class ConnectionInterfaceContactBlocking(dbus.service.Interface):
    """\
      An interface for connections where contacts can be blocked from
        communicating with this user and receiving this user's presence.
        Clients may retrieve a list of currently-blocked contacts using
        RequestBlockedContacts, and listen for
        BlockedContactsChanged to be notified
        when contacts are blocked and unblocked. The
        BlockContacts and
        UnblockContacts methods do what they say
        on the tin; depending on the value of the
        ContactBlockingCapabilities property,
        contacts may be reported for spam or other abuse when calling
        BlockContacts.

      This interface is intended for protocols where blocking contacts
        persists on the server between connections; connection managers for
        protocols with no server-side support for blocking contacts MAY choose
        to implement this interface using an on-disk file of blocked
        contacts or some other means to store blocked contacts between
        connections.

      This interface is intended to replace the
        ContactList
        channel with TargetHandleType
        List and TargetID "deny"
        (along with the ContactList and
        ContactGroups
        interfaces replacing other channels with TargetHandleType
        List and TargetHandleType
        Group, respectively).
    """

    def __init__(self):
        self._interfaces.add('org.freedesktop.Telepathy.Connection.Interface.ContactBlocking')

    @dbus.service.method('org.freedesktop.Telepathy.Connection.Interface.ContactBlocking', in_signature='aub', out_signature='')
    def BlockContacts(self, Contacts, Report_Abusive):
        """
        Direct the server to block some contacts. The precise effect is
          protocol-dependent, but SHOULD include ignoring all current and
          subsequent communications from the given contacts, avoiding sending
          presence to them in future, and if they were already receiving the
          local user's presence, behaving as if the local user went
          offline.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Connection.Interface.ContactBlocking', in_signature='au', out_signature='')
    def UnblockContacts(self, Contacts):
        """
        Direct the server to unblock some contacts.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Connection.Interface.ContactBlocking', in_signature='', out_signature='a{us}')
    def RequestBlockedContacts(self):
        """
        List the contacts that are blocked.

        Clients SHOULD allow a relatively long timeout for calls to this
          method, since on some protocols contact blocking is part of the
          contact list, which can take a significant time to retrieve.
      
        """
        raise NotImplementedError
  
    @dbus.service.signal('org.freedesktop.Telepathy.Connection.Interface.ContactBlocking', signature='a{us}a{us}')
    def BlockedContactsChanged(self, Blocked_Contacts, Unblocked_Contacts):
        """
        Emitted when the list of blocked contacts is first retrieved
          (before returning from any pending calls to
          RequestBlockedContacts), and
          whenever the list of blocked contacts subsequently changes.
      
        """
        pass
  