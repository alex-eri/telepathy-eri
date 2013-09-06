# -*- coding: utf-8 -*-
# Generated from the Telepathy spec
""" Copyright (C) 2010-2012 Collabora Limited 

    This library is free software; you can redistribute it and/or modify it
      under the terms of the GNU Lesser General Public License as published by
      the Free Software Foundation; either version 2.1 of the License, or (at
      your option) any later version.

    This library is distributed in the hope that it will be useful, but
      WITHOUT ANY WARRANTY; without even the implied warranty of
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser
      General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
      along with this library; if not, write to the Free Software Foundation,
      Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
  
"""

import dbus.service


class ConnectionInterfaceAddressing(dbus.service.Interface):
    """\
      This interface deals with the multiple address types that can
      refer to the same contact, such as vCard fields and URIs.

      It can be used to retrieve contacts with a specific addresses
        through GetContactsByVCardField and
        GetContactsByURI, as well as
        defining the various addressing methods for a given contact
        through this interface's contact attributes.
    """

    def __init__(self):
        self._interfaces.add('org.freedesktop.Telepathy.Connection.Interface.Addressing1')

    @dbus.service.method('org.freedesktop.Telepathy.Connection.Interface.Addressing1', in_signature='sasas', out_signature='a{su}a{ua{sv}}')
    def GetContactsByVCardField(self, Field, Addresses, Interfaces):
        """
        Request contacts and retrieve their attributes using a given field
          in their vCards.

        The connection manager should record that these handles are in
          use by the client who invokes this method, and must not
          deallocate the handles until the client disconnects from the
          bus or calls the
          Connection.ReleaseHandles
          method.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Connection.Interface.Addressing1', in_signature='asas', out_signature='a{su}a{ua{sv}}')
    def GetContactsByURI(self, URIs, Interfaces):
        """
        Request contacts and retrieve their attributes using URI addresses.

        The connection manager should record that these handles are in
          use by the client who invokes this method, and must not
          deallocate the handles until the client disconnects from the
          bus or calls the
          Connection.ReleaseHandles
          method.
      
        """
        raise NotImplementedError
  