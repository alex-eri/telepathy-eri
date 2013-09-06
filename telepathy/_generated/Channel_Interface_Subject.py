# -*- coding: utf-8 -*-
# Generated from the Telepathy spec
"""Copyright © 2010–2011 Collabora Ltd.

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


class ChannelInterfaceSubject(dbus.service.Interface):
    """\
      An interface channels can implement to support subjects. Most
        of the time this will be implemented by channels implementing
        the Room2
        interface, but some protocols support subjects in 1-to-1 chats
        (such as XMPP). Note that this interface is not restricted to
        Text channels, and can also be used on Call channels.
    """

    def __init__(self):
        self._interfaces.add('org.freedesktop.Telepathy.Channel.Interface.Subject2')

    @dbus.service.method('org.freedesktop.Telepathy.Channel.Interface.Subject2', in_signature='s', out_signature='')
    def SetSubject(self, Subject):
        """
        Set the room's subject. Clients SHOULD look at the subject
          flags before calling this method as the user might not have
          permission to set the subject.

        A successful return of this method indicates a successful
          change in subject, but clients should still listen for changes
          to the Subject property for
          further changes by other users or the server.
      
        """
        raise NotImplementedError
  