import telepathy, dbus

__author__ = 'eri'

class vkCapabilities(
    telepathy.server.ConnectionInterfaceCapabilities,
    telepathy.server.ConnectionInterfaceContactCapabilities
):

    text_chat_class = \
        ({telepathy.CHANNEL_INTERFACE + '.ChannelType':
              telepathy.CHANNEL_TYPE_TEXT,
          telepathy.CHANNEL_INTERFACE + '.TargetHandleType':
              dbus.UInt32(telepathy.HANDLE_TYPE_CONTACT)},

         [telepathy.CHANNEL_INTERFACE + '.TargetHandle',
          telepathy.CHANNEL_INTERFACE + '.TargetID'])

    def __init__(self):
        telepathy.server.ConnectionInterfaceCapabilities.__init__(self)
        telepathy.server.ConnectionInterfaceContactCapabilities.__init__(self)

    def _set_caps(self,handles):
        caps = {}
        for handle in handles:
            if handle not in self._contact_caps:
                contact_caps = []
                contact_caps.append(self.text_chat_class)
                caps[handle] = contact_caps
        if caps:
            ret = dbus.Dictionary(caps, signature='ua(a{sv}as)')
            self.ContactCapabilitiesChanged(ret)
            self._contact_caps.update(caps)
