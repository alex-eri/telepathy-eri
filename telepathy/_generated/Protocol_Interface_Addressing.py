# -*- coding: utf-8 -*-
# Generated from the Telepathy spec
"""Copyright © 2010 Collabora Ltd.

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
      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
      02110-1301, USA.
  
"""

import dbus.service


class ProtocolInterfaceAddressing(dbus.service.Interface):
    """\
      An interface for protocols that support multiple forms of
        addressing contacts, for example through vCard addresses and URIs.

      If the ConnectionManager has a .manager file, and it
        supports this interface, the interface's immutable properties
        must be represented in the file; the representation is described as
        part of the documentation for each property.

      For instance, a SIP connection manager might have the
        following lines in the .manager file.


[Protocol sip]
AddressableVCardFields=tel;x-sip;
AddressableURISchemes=tel;sip;

    """

    def __init__(self):
        self._interfaces.add('org.freedesktop.Telepathy.Protocol.Interface.Addressing')

    @dbus.service.method('org.freedesktop.Telepathy.Protocol.Interface.Addressing', in_signature='ss', out_signature='s')
    def NormalizeVCardAddress(self, VCard_Field, VCard_Address):
        """
        Attempt to normalize the given vCard address. Where possible, this
          SHOULD return an address that would appear in the
          org.freedesktop.Telepathy.Connection.Interface.Addressing1/addresses
          attribute for a contact on a connected
          Connection.
        

        If full normalization requires network activity or is otherwise
          impossible to do without a Connection,
          this method SHOULD perform a best-effort normalization.

        An example would be a vCard TEL field with a formatted
          number in the form of +1 (206) 555 1234, this would be
          normalized to +12065551234.

        This method MAY simply raise NotImplemented on some
        protocols, if it has no use.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Protocol.Interface.Addressing', in_signature='s', out_signature='s')
    def NormalizeContactURI(self, URI):
        """
        Attempt to normalize the given contact URI. Where possible, this
          SHOULD return an address that would appear in the
          org.freedesktop.Telepathy.Connection.Interface.Addressing1/uris
          attribute for a contact on a connected
          Connection.
        

        If full normalization requires network activity or is otherwise
          impossible to do without a Connection,
          this method SHOULD perform a best-effort normalization.

        If the URI has extra information beyond what's necessary to
          identify a particular contact, such as an XMPP resource or an
          action to carry out, this extra information SHOULD be removed.
          If all URIs in a scheme contain a verb or action
          (like aim, ymsgr and
          msnim URIs), then the verb SHOULD be replaced
          with the one specified in
          AddressableURISchemes.

        
          This method is intended to normalize URIs stored in address
            books, for instance. In protocols like XMPP, if you
            vary the resource or action (query string), the URI still
            refers to the same high-level contact.
        

        For instance,
          xmpp:romeo@Example.Com/Empathy?message;body=Hello
          would be normalized to xmpp:romeo@example.com,
          and aim:goim?screenname=Romeo%20M&message=Hello
          would be normalized to
          aim:addbuddy?screenname=romeom.

        This method MAY simply raise NotImplemented on some
        protocols, if it has no use.
      
        """
        raise NotImplementedError
  