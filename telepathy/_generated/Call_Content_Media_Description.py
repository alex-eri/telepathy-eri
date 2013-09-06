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


class CallContentMediaDescription(dbus.service.Object):
    """\
      This object represents a remote Description Offer to which the local
      streaming implementation should reply with its local Description.

      This is intended as a temporary transactional object for use with Content.Interface.Media.
      There will always be 0 or 1 MediaDescription object per Content.
      In most cases, this object will stay alive until you call either
      Accept or
      Reject, and then disappear.
      There are some cases (e.g. an endpoint being removed from the call)
      where a MediaDescription object will disappear before you have had a
      chance to either Accept or Reject it.
    """

    @dbus.service.method('org.freedesktop.Telepathy.Call1.Content.MediaDescription', in_signature='a{sv}', out_signature='')
    def Accept(self, Local_Media_Description):
        """
        Accepts the updated Description and update the corresponding
        local description. If FurtherNegotiationRequired is True,
        calling this method will generally cause a network round-trip
        and a new MediaDescription to be offered (hopefully with
        FurtherNegotiationRequired set to False).
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Content.MediaDescription', in_signature='(uuss)', out_signature='')
    def Reject(self, Reason):
        """
        Reject the proposed update to the remote description.
      
        """
        raise NotImplementedError
  