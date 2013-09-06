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

from telepathy.client.channel import Channel
from telepathy.client.interfacefactory import (
    InterfaceFactory, default_error_handler)
from telepathy.interfaces import (
    CONN_INTERFACE, CONNECTION_INTERFACE_REQUESTS)
from telepathy.constants import CONNECTION_STATUS_CONNECTED


class Connection(InterfaceFactory):
    def __init__(self, service_name, object_path=None, bus=None,
            ready_handler=None, error_handler=default_error_handler):
        if not bus:
            self.bus = dbus.Bus()
        else:
            self.bus = bus

        if object_path is None:
            object_path = '/' + service_name.replace('.', '/')

        self.service_name = service_name
        self.object_path = object_path
        self._ready_handlers = []
        if ready_handler is not None:
            self._ready_handlers.append(ready_handler)
        self._error_handler = error_handler
        self._ready = False

        object = self.bus.get_object(service_name, object_path)
        InterfaceFactory.__init__(self, object, CONN_INTERFACE)

        # note: old dbus-python returns None from connect_to_signal
        self._status_changed_connection = \
            self[CONN_INTERFACE].connect_to_signal('StatusChanged',
                lambda status, reason: self._status_cb(status))
        self[CONN_INTERFACE].GetStatus(
            reply_handler=self._status_cb,
            error_handler=error_handler)

    def _status_cb(self, status):
        if status == CONNECTION_STATUS_CONNECTED:
            self._get_interfaces()

            if self._status_changed_connection:
                # disconnect signal handler
                self._status_changed_connection.remove()
                self._status_changed_connection = None

    def _get_interfaces(self):
        self[CONN_INTERFACE].GetInterfaces(
            reply_handler=self._get_interfaces_reply_cb,
            error_handler=self._error_handler)

    def _get_interfaces_reply_cb(self, interfaces):
        if self._ready:
            return

        self._ready = True

        self.get_valid_interfaces().update(interfaces)

        for ready_handler in self._ready_handlers:
            ready_handler(self)

    @staticmethod
    def get_connections(bus=None):
        connections = []
        if not bus:
            bus = dbus.Bus()

        bus_object = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')

        for service in bus_object.ListNames(dbus_interface='org.freedesktop.DBus'):
            if service.startswith('org.freedesktop.Telepathy.Connection.'):
                connection = Connection(service, "/%s" % service.replace(".", "/"), bus)
                connections.append(connection)

        return connections

    def request_channel(self, type, handle_type, handle, suppress_handler):
        path = self.RequestChannel(type, handle_type, handle, suppress_handler)
        return Channel(self.service_name, path, self.bus)

    def create_channel(self, props):
        object_path, props = self[CONNECTION_INTERFACE_REQUESTS].CreateChannel(props)
        return Channel(self.service_name, object_path, self.bus)

    def call_when_ready(self, handler):
        if self._ready:
            handler(self)
        else:
            self._ready_handlers.append(handler)
