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


class CallContent(dbus.service.Object):
    """\
      This object represents one Content inside a Call1. For
      example, in an audio/video call there would be one audio content
      and one video content. Each content has one or more Stream objects which
      represent the actual transport to one or more remote contacts.
      
        There are two cases where multiple streams may happen:
        
          Calls with more than two participants, if the protocol does not
          support multicast, and does not have mixer proxy.
          With jingle, when calling a contact connected from multiple
          resources, a stream is created for each resource. Once the remote
          contact answered from one of its resources, all other streams get
          removed.
        
      
      For protocols that support muting all streams of a given content
      separately, this object MAY also implement the Mute interface
    """

    @dbus.service.method('org.freedesktop.Telepathy.Call1.Content', in_signature='', out_signature='')
    def Remove(self):
        """
        Remove the content from the call. This will cause
        Call1.ContentRemoved((self_handle,
        User_Requested, "", "")) to be
        emitted.
      
        """
        raise NotImplementedError
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Content', signature='ao')
    def StreamsAdded(self, Streams):
        """
         Emitted when streams are added to a call.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Content', signature='ao(uuss)')
    def StreamsRemoved(self, Streams, Reason):
        """
         Emitted when streams are removed from a call
      
        """
        pass
  