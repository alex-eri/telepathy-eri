# telepathy-python - Base classes defining the interfaces of the Telepathy framework
#
# Copyright (C) 2005,2006 Collabora Limited
# Copyright (C) 2005,2006 Nokia Corporation
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

from telepathy._generated.constants import *

# Backwards compatibility
CONNECTION_HANDLE_TYPE_NONE = HANDLE_TYPE_NONE
CONNECTION_HANDLE_TYPE_CONTACT = HANDLE_TYPE_CONTACT
CONNECTION_HANDLE_TYPE_ROOM = HANDLE_TYPE_ROOM
CONNECTION_HANDLE_TYPE_LIST = HANDLE_TYPE_LIST
CONNECTION_HANDLE_TYPE_USER_CONTACT_GROUP = HANDLE_TYPE_GROUP

# Connection_Presence_Status_Identifier
CONNECTION_PRESENCE_STATUS_AVAILABLE = "available"
CONNECTION_PRESENCE_STATUS_CHAT = "chat"
CONNECTION_PRESENCE_STATUS_PSTN = "pstn"
CONNECTION_PRESENCE_STATUS_AWAY = "away"
CONNECTION_PRESENCE_STATUS_BRB = "brb"
CONNECTION_PRESENCE_STATUS_BUSY = "busy"
CONNECTION_PRESENCE_STATUS_DND = "dnd"
CONNECTION_PRESENCE_STATUS_EXTENDED_AWAY = "xa"
CONNECTION_PRESENCE_STATUS_HIDDEN = "hidden"
CONNECTION_PRESENCE_STATUS_OFFLINE = "offline"
CONNECTION_PRESENCE_STATUS_UNKNOWN = "unknown"
CONNECTION_PRESENCE_STATUS_ERROR = "error"
