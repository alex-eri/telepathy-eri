import logging
import dbus

import telepathy
from utils.decorators import loggit

__all__ = ['EriChannel']

logger = logging.getLogger('Eri.channel')

class EriChannel(object):
    @loggit(logger)
    def __init__(self, conn, props):

        logger.debug(str(props))

        # If we have InitiatorHandle set in our new channel, use that,
        if telepathy.CHANNEL_INTERFACE + '.InitiatorHandle' in props:
            self._initiator = conn.handle(telepathy.HANDLE_TYPE_CONTACT,
                props[telepathy.CHANNEL_INTERFACE + '.InitiatorHandle'])

        # otherwise use InitiatorID.
        elif telepathy.CHANNEL_INTERFACE + '.InitiatorID' in props:
            self._initiator = conn.ensure_handle(telepathy.HANDLE_TYPE_CONTACT,
                props[telepathy.CHANNEL_INTERFACE + '.InitiatorID'])

        # If we don't have either of the above but we requested the channel,
        # then we're the initiator.
        elif props[telepathy.CHANNEL_INTERFACE + '.Requested']:
            self._initiator = conn.GetSelfHandle()

        else:
            logger.warning('InitiatorID or InitiatorHandle not set on new channel')
            self._initiator = None

        # Don't implement the initiator properties if we don't have one.
        if self._initiator:
            self._implement_property_get(telepathy.CHANNEL_INTERFACE, {
                    'InitiatorHandle': loggit(logger,'InitiatorHandle')(lambda: dbus.UInt32(self._initiator.id)),
                    'InitiatorID': loggit(logger,'InitiatorID')(lambda: self._initiator.name)
                    })

            self._add_immutable_properties({
                    'InitiatorHandle': telepathy.CHANNEL_INTERFACE,
                    'InitiatorID': telepathy.CHANNEL_INTERFACE,
                    })
