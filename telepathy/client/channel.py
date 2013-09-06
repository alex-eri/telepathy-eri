# telepathy-python - Base classes defining the interfaces of the Telepathy framework
#
# Copyright (C) 2005, 2006 Collabora Limited
# Copyright (C) 2005, 2006 Nokia Corporation
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import dbus

from telepathy.client.interfacefactory import (
    InterfaceFactory, default_error_handler)
from telepathy.interfaces import CHANNEL_INTERFACE

class Channel(InterfaceFactory):
    def __init__(self, service_name, object_path, bus=None, ready_handler=None,
                 error_handler=default_error_handler):
        if not bus:
            bus = dbus.Bus()

        self.service_name = service_name
        self.object_path = object_path
        self._ready_handler = ready_handler
        self.error_cb = error_handler
        object = bus.get_object(service_name, object_path)
        InterfaceFactory.__init__(self, object, CHANNEL_INTERFACE)

        if ready_handler:
            self[CHANNEL_INTERFACE].GetChannelType(
                reply_handler=self.get_channel_type_reply_cb,
                error_handler=self.error_cb)
        else:
            type = self.GetChannelType()
            interfaces = self.GetInterfaces()
            self.get_valid_interfaces().add(type)
            self.get_valid_interfaces().update(interfaces)

    def get_channel_type_reply_cb(self, interface):
        self.get_valid_interfaces().add(interface)
        self[CHANNEL_INTERFACE].GetInterfaces(
            reply_handler=self.get_interfaces_reply_cb,
            error_handler=self.error_cb)

    def get_interfaces_reply_cb(self, interfaces):
        self.get_valid_interfaces().update(interfaces)
        if self._ready_handler is not None:
            self._ready_handler(self)
