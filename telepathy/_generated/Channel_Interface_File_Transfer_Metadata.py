# -*- coding: utf-8 -*-
# Generated from the Telepathy spec
"""Copyright (C) 2011 Collabora Ltd.

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
      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
      USA.
  
"""

import dbus.service


class ChannelInterfaceFileTransferMetadata(dbus.service.Interface):
    """\
      This interface exists to provide a mechanism to include
        arbitrary additional information in file transfers. For
        example, one might want to send a document and include the
        number of times the character P appeared in the file, so would
        add NumberOfPs=42 to the
        Metadata property.

      ServiceName living in its own
        property makes it easier for specific applications to send
        files to each other, bypassing the standard handler. For
        example, the Banshee Telepathy plugin handler could match on
        ServiceName so the Empathy file
        transfer is not used instead.
   """

    def __init__(self):
        self._interfaces.add('org.freedesktop.Telepathy.Channel.Interface.FileTransfer.Metadata')
