# -*- coding: utf-8 -*-
# Generated from the Telepathy spec
"""Copyright © 2011 Collabora Ltd.

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


class ChannelInterfaceRoomConfig(dbus.service.Interface):
    """\
      Represents the configuration of a chatroom, some aspects of which may
        be modifiable by the user, depending on their privileges. This
        corresponds to the room configuration on XMPP, and various channel mode
        flags on IRC.

      The “topic” (on IRC) or “subject” (on XMPP) is not part of this
        interface; it can be found on the Subject2
        interface.
    """

    def __init__(self):
        self._interfaces.add('org.freedesktop.Telepathy.Channel.Interface.RoomConfig1')

    @dbus.service.method('org.freedesktop.Telepathy.Channel.Interface.RoomConfig1', in_signature='a{sv}', out_signature='')
    def UpdateConfiguration(self, Properties):
        """
        If CanUpdateConfiguration is
          True, modifies the current values of one or more
          room properties. This method SHOULD NOT return until the change has
          been accepted or declined by the server.

        Note that the server may ostensibly accept the changes (thus
          allowing this method to return success) but signal different values;
          for example, the server might truncate
          Title to some maximum length. Callers
          SHOULD continue to listen for the PropertiesChanged
          signal, and trust the values it signals over those provided to this
          method.
      
        """
        raise NotImplementedError
  