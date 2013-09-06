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


class CallContentInterfaceVideoControl(dbus.service.Interface):
    """\
      An interface that allows the connection manager to control the video
          stream.
      This interface is generally not needed. In cases where the connection
          manager handles the network communication and the media is transferred
          from the client to the connection manager via shared memory, it can
          sometimes be beneficial for the connection manager to be able to
          control certain aspects of the video stream.
    """

    def __init__(self):
        self._interfaces.add('org.freedesktop.Telepathy.Call1.Content.Interface.VideoControl')

    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Content.Interface.VideoControl', signature='')
    def KeyFrameRequested(self):
        """
        Request that the video encoder produce a new key frame as soon as
        possible.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Content.Interface.VideoControl', signature='(uu)')
    def VideoResolutionChanged(self, NewResolution):
        """
        The desired video resolution has changed.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Content.Interface.VideoControl', signature='u')
    def BitrateChanged(self, NewBitrate):
        """
        The desired bitrate has changed
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Content.Interface.VideoControl', signature='u')
    def FramerateChanged(self, NewFramerate):
        """
        The desired framerate has changed
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Content.Interface.VideoControl', signature='u')
    def MTUChanged(self, NewMTU):
        """
        The Maximum Transmission Unit has changed
      
        """
        pass
  