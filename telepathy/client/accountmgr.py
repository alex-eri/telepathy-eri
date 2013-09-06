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

from telepathy.client.interfacefactory import (InterfaceFactory,
                                               default_error_handler)
from telepathy.interfaces import ACCOUNT_MANAGER

class AccountManager(InterfaceFactory):
    def __init__(self, bus=None, ready_handler=None,
            error_handler=default_error_handler):
        if not bus:
            bus = dbus.Bus()

        self.service_name = ACCOUNT_MANAGER
        self.object_path = '/org/freedesktop/Telepathy/AccountManager'
        self._ready_handler = ready_handler
        self._error_cb = error_handler
        object = bus.get_object(self.service_name, self.object_path)
        InterfaceFactory.__init__(self, object, ACCOUNT_MANAGER)

        self[dbus.PROPERTIES_IFACE].Get(
            ACCOUNT_MANAGER,
            'Interfaces',
            reply_handler=self._get_interfaces_cb,
            error_handler=self._error_cb)

    def _get_interfaces_cb(self, interfaces):
        self.get_valid_interfaces().update(interfaces)
        if self._ready_handler:
            self._ready_handler(self)
