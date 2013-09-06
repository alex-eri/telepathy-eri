# -*- coding: utf-8 -*-
# Generated from the Telepathy spec
"""Copyright © 2010 Collabora Ltd.
Copyright © 2010 Nokia Corporation

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


class ChannelInterfaceRoom(dbus.service.Interface):
    """\
      Different IM protocols use a variety of ways to name chat rooms. The
        simplest example is perhaps IRC, where chat rooms have short,
        persistent, human-readable string names, and are generally global
        across the network. Skype chat rooms have persistent string names, so
        you can leave and re-join a room, but these names are opaque unique
        identifiers. MSN chat rooms are unnamed, and you can only join one by
        being invited. And XMPP wins the coveted “most complicated chat rooms”
        prize: chat rooms may be hosted by different servers with different DNS
        names; normally they have human-readable names, except that all MUCs on
        Google Talk's conference server have UUIDs as names, and XEP-0045 §10.1.4
        Requesting a Unique Room Name defines a protocol for
        requesting a unique, opaque room name on the server. Note that
        this interface is not restricted to Text channels, and can
        also be used on Call channels.

      This interface intends to support and differentiate these mechanisms
        more clearly than the TargetHandleType
        and TargetID
        properties can alone. It initially contains a pair of properties used
        to represent the human-readable parts of a
        Room_Handle's identifier, if any. The above examples
        for different protocols are represented as follows:

      
        The IRC channel #telepathy on Freenode is represented by a
          channel with properties
          TargetHandleType
          = Room,
          TargetID
          = "#telepathy",
          RoomName = "#telepathy",
          Server = "", indicating
          that the room has a human-readable identifier, and is not confined to
          a particular server on the network.

          
            Actually, IRC supports creating “local” channels specific to the
            server they are created on. These channels have identifiers
            starting with & rather than #. These could be
            represented by setting Server
            appropriately.
          
        

        A Skype group chat with opaque identifier 0xdeadbeef has
          TargetHandleType
          = Room,
          TargetID
          = "0xdeadbeef",
          RoomName = "",
          Server = "", indicating
          that the room has an identifier but no human-readable name.
        

        An MSN group chat has
          TargetHandleType
          = None,
          RoomName = "",
          Server = "", indicating
          that the room has neither an identifier (so it cannot be re-joined
          later) nor a human-readable name.
        

        A standard Jabber multi-user chat
          jdev@conference.jabber.org has
          TargetHandleType
          = Room,
          TargetID
          = "jdev@conference.jabber.org",
          RoomName = "jdev",
          Server = "conference.jabber.org".
        

        A Google Talk private MUC private-chat-11111x1x-11xx-111x-1111-111x1xx11x11@groupchat.google.com has
          TargetHandleType
          = Room,
          TargetID
          = "private-chat-11111x1x-11xx-111x-1111-111x1xx11x11@groupchat.google.com",
          RoomName = "",
          Server =
          "groupchat.google.com", indicating that the room has a
          persistent identifier, no human-readable name, and is hosted by a
          particular server.
        

        Similarly, a XEP-0045 §10.1.4 uniquely-named room
          lrcgsnthzvwm@conference.jabber.org has
          TargetHandleType
          = Room,
          TargetID
          = "lrcgsnthzvwm@conference.jabber.org",
          RoomName = "",
          Server =
          "conference.jabber.org", indicating that the room has a
          persistent identifier, no human-readable name, and is hosted by a
          particular server.
        
      

      Requestable channel classes

      If the connection supports joining text chat rooms by unique
        identifier, like Skype, it should advertise a
        Requestable_Channel_Class matching:

      
        
( Fixed = { ...ChannelType: ...Text,
            ...TargetHandleType: Room,
          },
  Allowed = [ ...TargetID,
              ...TargetHandle,
            ]
)

      Channel requests must specify either TargetID or TargetHandle.

      If, like IRC, the room identifiers are also human-readable, the
        RCCs should also include RoomName in Allowed_Properties:

      
        
( Fixed = { ...ChannelType: ...Text,
            ...TargetHandleType: Room,
          },
  Allowed = [ ...TargetID,
              ...TargetHandle,
              ...RoomName
            ]
),

( Fixed = { ...ChannelType: ...Text
          },
  Allowed = [ ...RoomName,
            ]
)

      Requests may specify the RoomName in place of
        TargetID or
        TargetHandle
        . Note how RoomName appears
        in Allowed_Properties of a different RCC because
        when TargetHandleType is omitted (or is None), both
        TargetHandle and
        TargetID must also be omitted.
        RoomName is allowed in conjuction
        with
        TargetID or
        TargetHandle
        in some situations, as explained below in the Requesting room
        channels section.
      

      If rooms may be on different servers, Server
        should also be included in the allowed properties, but
        CMs MUST use a reasonable default
        Server if not explicitly
        specified in a channel request. The CM's default server MAY
        be configurable by a connection parameter specified on a
        RequestConnection call, similarly to how the
        fallback conference server is specified on jabber connections in
        gabble.

      If the protocol supports unnamed rooms, RoomName
        should be fixed to the empty string, and
        TargetHandleType
        should be None:

      
        
( Fixed = { ...ChannelType: ...Text,
            ...TargetHandleType: None,
            ...RoomName: "",
          },
  Allowed = [ ]
)

      Requesting room channels

      When explicitly joining a room, the CM cannot know whether the room
        ID is unique or not. As a result, if this is the case, adding an
        empty string RoomName into the channel
        request will ensure the CM knows. For example:

      
        
{ ...ChannelType: ...Text,
  ...TargetHandleType: Room,
  ...TargetID: "qwerasdfzxcv@conference.jabber.org",
  ...RoomName: ""
}

      If RoomName features in
        Allowed_Properties then the only value allowed in conjunction
        with TargetID
        or TargetHandle
        is the empty string. Requests with conflicting
        TargetID
        and RoomName properties
        will fail with InvalidArgument.

      To create a XEP-0045 §10.1.4 uniquely-named room channel
        on the conference.jabber.org server, then the following channel
        request should be made:

      
        
{ ...ChannelType: ...Text,
  ...RoomName: ""
  ...Server: "conference.jabber.org"
}
      

      If everything is successful, then when the channel request is
        satisfied, a new channel will appear with the following properties:

      
        
{ ...ChannelType: ...Text,
  ...TargetHandleType: Room,
  ...TargetID: "kajsdhkajshdfjkshdfjkhs@conference.jabber.org",
  ...RoomName: ""
  ...Server: "conference.jabber.org"
}
      

      The CM will have received the unique room name (kajsdhkajshdfjkshdfjkhs)
        and then created a room with such a name on the said server. The empty
        RoomName property shows that the room name
        is not human-readable.

    """

    def __init__(self):
        self._interfaces.add('org.freedesktop.Telepathy.Channel.Interface.Room2')
