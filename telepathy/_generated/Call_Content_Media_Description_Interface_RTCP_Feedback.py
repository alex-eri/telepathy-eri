# -*- coding: utf-8 -*-
# Generated from the Telepathy spec
""" Copyright © 2005-2010 Nokia Corporation 
 Copyright © 2005-2010 Collabora Ltd 

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
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
  
"""

import dbus.service


class CallContentMediaDescriptionInterfaceRTCPFeedback(dbus.service.Interface):
    """\
      This codec offer interface provides a method of signalling
        support for RTCP feedback, documented by Extended RTP
        Profile for Real-time Transport Control Protocol (RTCP)-Based
        Feedback (RTP/AVPF) (RFC 4585).

      The codec identifiers used in the description of the Feedback Messages
      sent in the Accept's
      should match those used for the RemoteCodecs in the same Accept call.
      

      For more details on what RTCP Feedback can do and how to use
        it, one should refer to
        RFC 4585.

    """

    def __init__(self):
        self._interfaces.add('org.freedesktop.Telepathy.Call1.Content.MediaDescription.Interface.RTCPFeedback')
