# -*- coding: utf-8 -*-
# Generated from the Telepathy spec
"""Copyright © 2009-2011 Collabora Ltd.

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


class CallContentInterfaceAudioControl(dbus.service.Interface):
    """\
      This interface allows the connection manager to be kept informed of,
          and control, the input and output volumes of an audio stream.
          While generally not needed, if the connection manager needs to
          handle stream volumes directly (typically when using
          Call_Content_Packetization_Type_Raw),
          this interface may be necessary.

      If this interface is present, the handler should call
          ReportInputVolume
          and ReportOutputVolume whenever the
          input and output volume change, both when the user manually modifies
          the volume and when the volumes are adjusted in response to
          RequestedInputVolume and
          RequestedOutputVolume changing.

      The maximum volume as used in this interface represent the unamplified
         hardware volume (0 dB). No software amplification should be used to
         boost the signal to a higher level when this Interface is in use
    """

    def __init__(self):
        self._interfaces.add('org.freedesktop.Telepathy.Call1.Content.Interface.AudioControl')

    @dbus.service.method('org.freedesktop.Telepathy.Call1.Content.Interface.AudioControl', in_signature='i', out_signature='')
    def ReportInputVolume(self, Volume):
        """
        Report to the CM that the Content input volume has been
          changed by the client.

        It is the client's responsibility to change the input volume used for
           the content. However, the client MUST call this whenever it changes
           input volume for the content.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Content.Interface.AudioControl', in_signature='i', out_signature='')
    def ReportOutputVolume(self, Volume):
        """
        Report to the CM that the content output volume has been
          changed by the client.

        It is the client's responsibility to change the output volume used
           for the content. However, the client MUST call this whenever it
           changes output volume for the content.
      
        """
        raise NotImplementedError
  