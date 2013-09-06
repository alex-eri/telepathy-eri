# telepathy-python - Base classes defining the interfaces of the Telepathy framework
#
# Copyright (C) 2005 Collabora Limited
# Copyright (C) 2005 Nokia Corporation
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

"""
Loads .manager files according to
http://telepathy.freedesktop.org/wiki/FileFormats.
"""

import ConfigParser, os
import dircache
import dbus
import telepathy


_dbus_py_version = getattr(dbus, 'version', (0,0,0))

def _convert_pathlist(pathlist):
    dirlist = pathlist.split(":")
    # Reverse so least-important is first
    dirlist.reverse()
    dirs = []
    for path in dirlist:
        if len(path):
            path = os.path.abspath(os.path.expanduser(path))
            dirs.append(os.path.join(path, "telepathy", "managers"))
    return dirs

class ManagerRegistry:
    def __init__(self, bus=None):
        self.services = {}
        self.bus = bus

    def LoadManager(self, path):
        config = ConfigParser.RawConfigParser()
        config.read(path)

        cm_name = os.path.basename(path)[:-len(".manager")]
        self.services[cm_name] = {
            "name": cm_name,
            "busname": "org.freedesktop.Telepathy.ConnectionManager.%s" % cm_name,
            "objectpath": "/org/freedesktop/Telepathy/ConnectionManager/%s" % cm_name,
        }
        protocols = {}

        for section in set(config.sections()):
            if section.startswith('Protocol '):
                proto_name = section[len('Protocol '):]
                protocols[proto_name] = dict(config.items(section))

        if not protocols:
            raise ConfigParser.NoSectionError("no protocols found (%s)" % path)

        self.services[cm_name]["protos"] = protocols

    def LoadManagers(self):
        """
        Searches local and system wide configurations

        Can raise all ConfigParser errors. Generally filename member will be
        set to the name of the erronous file.
        """

        # Later items in the list are _more_ important
        all_paths = []
        if os.environ.has_key("XDG_DATA_DIRS"):
            all_paths += _convert_pathlist(os.environ["XDG_DATA_DIRS"])
        else:
            all_paths.append('/usr/share/telepathy/managers')
            all_paths.append('/usr/local/share/telepathy/managers')

        home = os.path.expanduser("~")
        if os.environ.has_key("XDG_DATA_HOME"):
            all_paths += _convert_pathlist(os.environ["XDG_DATA_HOME"])
        else:
            all_paths.append(os.path.join(home, ".local", "share", \
                "telepathy", "managers"))

        all_paths.append(os.path.join(home, ".telepathy", "managers"))

        for path in all_paths:
            if os.path.exists(path):
                for name in dircache.listdir(path):
                    if name.endswith('.manager'):
                        self.LoadManager(os.path.join(path, name))

    def GetProtos(self):
        """
        returns a list of protocols supported on this system
        """
        protos=set()
        for service in self.services.keys():
            if self.services[service].has_key("protos"):
                protos.update(self.services[service]["protos"].keys())
        return list(protos)

    def GetManagers(self, proto):
        """
        Returns names of managers that can handle the given protocol.
        """
        managers = []
        for service in self.services.keys():
            if "protos" in self.services[service]:
                if self.services[service]["protos"].has_key(proto):
                    managers.append(service)
        return managers

    def GetBusName(self, manager):
        assert(manager in self.services)
        assert('busname' in self.services[manager])
        return self.services[manager]['busname']

    def GetObjectPath(self, manager):
        assert(manager in self.services)
        assert('objectpath' in self.services[manager])
        return self.services[manager]['objectpath']

    def GetManager(self, manager):
        return telepathy.client.ConnectionManager(
            self.services[manager]['busname'],
            self.services[manager]['objectpath'],
            bus = self.bus)

    def GetParams(self, manager, proto):
        """
        Returns a dict of paramters for the given proto on the given manager.
        The keys will be the parameters names, and the values a tuple of (dbus
        type, default value, flags). If no default value is specified, the
        second item in the tuple will be None.
        """

        params = {}
        config = self.services[manager]["protos"][proto]

        for key, val in config.iteritems():
            if not key.startswith('param-'):
                continue

            name = key[len('param-'):]
            values = val.split()
            type = values[0]
            flags = 0
            default = None

            if "register" in values:
                flags |= telepathy.CONN_MGR_PARAM_FLAG_REGISTER

            if "required" in values:
                flags |= telepathy.CONN_MGR_PARAM_FLAG_REQUIRED

            for key, val in config.iteritems():
                if key.strip().startswith("default-"+name):
                    if _dbus_py_version < (0, 80):
                        default = dbus.Variant(val.strip(), signature=type)
                    else:
                        default = val.strip()
                        if type in 'uiqntxy':
                            default = int(default)
                        elif type == 'b':
                            if default.lower() in ('0', 'false'):
                                default = False
                            else:
                                default = True
                        elif type == 'd':
                            default = float(default)
                        # we don't support non-basic types
                    flags |= telepathy.CONN_MGR_PARAM_FLAG_HAS_DEFAULT

            params[name] = (type, default, flags)

        return params
