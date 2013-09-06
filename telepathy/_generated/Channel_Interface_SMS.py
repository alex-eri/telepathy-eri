# -*- coding: utf-8 -*-
# Generated from the Telepathy spec
"""Copyright © 2008–2010 Nokia Corporation
Copyright © 2010 Collabora Ltd.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
  
"""

import dbus.service


class ChannelInterfaceSMS(dbus.service.Interface):
    """\
      This interface contains SMS-specific properties for text
        channels.

      The presence of this interface on a channel does not imply that
        messages will be delivered via SMS.

      This interface MAY appear in the
        Interfaces property
        of channels where SMSChannel would be
        immutable and false. It SHOULD appear on channels where
        SMSChannel is immutable and true, and
        also on channels where SMSChannel is
        mutable (i.e. channels that might fall back to sending SMS at any
        time, such as on MSN).

      Handler filters

      A handler for class 0 SMSes should advertise the following filter:

      
{ ...ChannelType:
      ...Text,
  ...TargetHandleType:
      Contact,
  ...SMS.Flash:
      True,
}

      It should also set its BypassApproval property
        to True, so that it is invoked immediately for new
        channels.

      Contact Capabilities

      Contacts to whom SMSes can be sent SHOULD indicate this via a
        requestable channel class with
        SMSChannel = True as a fixed
        property.

      For instance, a contact that can accept both text and SMS channels:

      
[
 ({ ...ChannelType:
     ...Text,
    ...TargetHandleType:
       Contact,
  },
  [ ...TargetHandle,
    ...TargetID ]),

 ({ ...ChannelType:
       ...Text,
    ...TargetHandleType:
       Contact,
    ...SMSChannel: True,
  },
  [ ...TargetHandle,
    ...TargetID ]),
]
      
    """

    def __init__(self):
        self._interfaces.add('org.freedesktop.Telepathy.Channel.Interface.SMS')

    @dbus.service.method('org.freedesktop.Telepathy.Channel.Interface.SMS', in_signature='aa{sv}', out_signature='uii')
    def GetSMSLength(self, Message):
        """
        Returns the number of 140 octet chunks required to send a message
          via SMS, as well as the number of remaining characters available in
          the final chunk and, if possible, an estimate of the cost.

        
          There are a number of different SMS encoding mechanisms, and the
            client doesn't know which mechanisms an individual CM might support.
            This method allows the client, without any knowledge of the
            encoding mechanism, to provide length details to the user.
        

        Clients SHOULD limit the frequency with which this method is called
        and SHOULD NOT call it for every keystroke. Clients MAY estimate the
        remaining size between single keystrokes.
      
        """
        raise NotImplementedError
  
    @dbus.service.signal('org.freedesktop.Telepathy.Channel.Interface.SMS', signature='b')
    def SMSChannelChanged(self, SMSChannel):
        """
        This signal indicates a change in the
        SMSChannel property.
      
        """
        pass
  