# -*- coding: utf-8 -*-
# Generated from the Telepathy spec
"""Copyright © 2009-2010 Collabora Ltd.
Copyright © 2009-2010 Nokia Corporation

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


class CallStream(dbus.service.Object):
    """\
      One stream inside a Content.  A stream is
      a single flow of packets to and from a single remote endpoint.
      If your call connects to multiple people, you could have
      multiple streams.
      For protocols that support muting streams separately, this object MAY
      also implement the Mute interface
    """

    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream', in_signature='b', out_signature='')
    def SetSending(self, Send):
        """
        Set the stream to start or stop sending media from the local
        user to other contacts.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream', in_signature='ub', out_signature='')
    def RequestReceiving(self, Contact, Receive):
        """
        Request that a remote contact stops or starts sending on
          this stream.

        The CanRequestReceiving
          property defines whether the protocol allows the local user to
          request the other side start sending on this stream.
      
        """
        raise NotImplementedError
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream', signature='a{uu}a{us}au(uuss)')
    def RemoteMembersChanged(self, Updates, Identifiers, Removed, Reason):
        """
        Emitted when RemoteMembers changes.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream', signature='u(uuss)')
    def LocalSendingStateChanged(self, State, Reason):
        """
        Emitted when LocalSendingState changes.
      
        """
        pass
  