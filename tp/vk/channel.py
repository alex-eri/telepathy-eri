#!/usr/bin/python
# coding:utf-8
import weakref
import gobject
from tp.channel import EriChannel
from utils.decorators import loggit
import vkcom

__author__ = 'eri'

from time import time
from telepathy.server import ChannelTypeText,ChannelTypeContactList,ChannelInterfaceChatState,ChannelInterfaceMessages

import telepathy
import logging
logger = logging.getLogger('Eri.Vk/channel')

from utils.text import striphtml

import dbus
import dbus.service

class vkTextChannel(
    ChannelTypeText,
    ChannelInterfaceChatState,
    ChannelInterfaceMessages,
    EriChannel
):


    _message_part_support_flags = 0
    _delivery_reporting_support = 0

    _supported_content_types = ['text/plain','text/html', 'image/jpeg', 'image/png']
    _message_types = [telepathy.CHANNEL_TEXT_MESSAGE_TYPE_NORMAL, telepathy.CHANNEL_TEXT_MESSAGE_TYPE_DELIVERY_REPORT]

    def __init__(self, connection, manager, props, object_path=None):
        logger.debug('__init__')
        ChannelTypeText.__init__(self, connection, manager, props, object_path)
        EriChannel.__init__(self,connection,props)
        ChannelInterfaceChatState.__init__(self)
        ChannelInterfaceMessages.__init__(self)

        # telepathy.CONNECTION_INTERFACE_CONTACTS,
        #     {'ContactAttributeInterfaces' :
        #     lambda:  dbus.Array([telepathy.CONNECTION], signature='s')}

        logger.debug('init2')

        self._send_typing_notification_timeout = 0

        logger.debug('init3')
        self.states = {}
        self._implement_property_get(telepathy.CHANNEL_INTERFACE_CHAT_STATE,{
            'ChatStates' : loggit(logger,'ChatStates')(lambda: dbus.Dictionary(self.states, signature='uu'))
        })
        logger.debug('init4')



    @loggit(logger)
    def GetPendingMessageContent(self, Message_ID, Parts):
        return self._pending_IM_messages[Message_ID]

    def message_sent(self,message_id,uid,timestamp,title,text,attachments):
        message_type = telepathy.CHANNEL_TEXT_MESSAGE_TYPE_NORMAL
        headers = {
            'message-sent': timestamp,
            'message-type': message_type
        }
        body = {
            'content-type': 'text/plain',
            'content': striphtml(text)
        }
        message = [headers, body]
        self.Sent(timestamp, message_type, text)
        self.MessageSent(dbus.Array(message, signature='a{sv}'), 0, dbus.String(message_id))


    def message_received(self,message_id,uid,timestamp,title,text,attachments):
        self.Received(message_id,timestamp,self._handle.get_id(),telepathy.CHANNEL_TEXT_MESSAGE_TYPE_NORMAL,0,text)

        headers = dbus.Dictionary({
                   dbus.String('message-sent') : dbus.UInt64(timestamp),
                   dbus.String('message-received') : dbus.UInt64(time()),
                   dbus.String('pending-message-id') : dbus.UInt32(message_id),
                   dbus.String('message-token') : dbus.UInt32(message_id),
                   dbus.String('message-sender') : dbus.UInt32(self._handle.get_id()),
                   dbus.String('message-sender-id') : dbus.String(uid),
                   dbus.String('sender-nickname') : dbus.String(self._handle.contact.get('screen_name', uid)),
                   dbus.String('message-type') : dbus.UInt32(telepathy.CHANNEL_TEXT_MESSAGE_TYPE_NORMAL)
                  }, signature='sv')
        body = [headers]

        plain_text = striphtml(text)
        html = u'<p>{}</p>'.format(text)

        if attachments:

            photo_fields = [name[:-5] for name,value in attachments.items() if name[-5:]=='_type' and value == 'photo' ]
            # photos = [value for name,value in attachments.items() if name in photo_fields]

            photos = [attachments.get(k) for k in photo_fields if attachments.get(k)]
            if photos:
                try:
                    photos = self._conn.Api.photos.getById(photos=photos,photo_sizes=1)

                    for photo in photos:
                        logger.info(repr(photo))
                        for size in photo.get('sizes',[]):
                            if size.get('type') == 'x':
                                photo['src'] = size.get('src')
                                break
                        else:
                            size = photo.get('sizes',[None])[-1]
                            if size:
                                photo['src'] =  size.get('src')

                        identifier = 'photo{owner_id}_{id}'.format(**photo)
                        body.append( dbus.Dictionary({
                            dbus.String('content-type'): dbus.String('image/jpeg'),
                            dbus.String('needs-retrieval'): True,
                            dbus.String('identifier'): dbus.String(identifier)
                           }, signature='sv')
                        )
                        plain_text += u'\n{src}'.format(**photo)
                        # plain_text += u'<img src="{src}" alt="photo{owner_id}_{id}"/>'.format(**photo)
                        html += u'<br/><img src="cid:photo{owner_id}_{id}" alt="photo{owner_id}_{id}"/>'.format(**photo)

                except vkcom.APIError,e:
                    # att = u'\nAttachment Error: {}'.format(e.message)
                    att = u'Есть вложения, смотри https://vk.com/im?sel={}'.format(uid)
                    plain_text += att
                    html += '<br/>' + att

        #    body.append( dbus.Dictionary({
        #            dbus.String('alternative'): dbus.String('text'),
        #            dbus.String('content-type'): dbus.String('text/html'),
        #            dbus.String('content'): dbus.String(html)
        #           }, signature='sv')
        #    )
        #
        #    body.append( dbus.Dictionary({
        #            dbus.String('alternative'): dbus.String('text'),
        #            dbus.String('content-type'): dbus.String('text/plain'),
        #            dbus.String('content'): dbus.String(plain_text)
        #           }, signature='sv')
        #    )
        #
        #else:
        #    body.append( dbus.Dictionary({
        #            dbus.String('content-type'): dbus.String('text/plain'),
        #            dbus.String('content'): dbus.String(text)
        #           }, signature='sv')
        #    )


        body.append( dbus.Dictionary({
                dbus.String('alternative'): dbus.String('text'),
                dbus.String('content-type'): dbus.String('text/html'),
                dbus.String('content'): dbus.String(html)
               }, signature='sv')
        )

        body.append( dbus.Dictionary({
                dbus.String('alternative'): dbus.String('text'),
                dbus.String('content-type'): dbus.String('text/plain'),
                dbus.String('content'): dbus.String(plain_text)
               }, signature='sv')
        )

        message = dbus.Array(body, signature='a{sv}')

        self.MessageReceived(message)


    def Send(self, message_type, text):
        logger.debug('Send')
        if message_type != telepathy.CHANNEL_TEXT_MESSAGE_TYPE_NORMAL:
                logger.error('Unhandled message type: {}'.format(message_type))
                raise telepathy.NotImplemented("Unhandled message type")
        message_id = self._send_text_message(self._handle.name, text)
        return dbus.String(message_id)


    def _send_text_message(self, to, text,plain=True):
        logger.debug(text)
        if plain:
            text=text.replace('<','&lt;')
        return self._conn.send_text(to,text)

    @loggit(logger)
    def SendMessage(self, message, flags):
        headers = message.pop(0)
        message_type = int(headers.get('message-type', telepathy.CHANNEL_TEXT_MESSAGE_TYPE_NORMAL))
        if message_type != telepathy.CHANNEL_TEXT_MESSAGE_TYPE_NORMAL:
                raise telepathy.NotImplemented("Unhandled message type")
        text = None

        #TODO html
        for part in message:
            if part.get("content-type", None) ==  "text/plain":
                text = part['content']
                break
        if text is None:
                raise telepathy.NotImplemented("Unhandled message type")

        message_id = self._send_text_message(self._handle.name, text)
        return  dbus.String(message_id)


    @loggit(logger)
    def SetChatState(self, State):
            self.states[self._conn._self_handle] = State

            if State == telepathy.CHANNEL_CHAT_STATE_COMPOSING:
                # User has started typing.
                self.send_typing_notification()

                # If we haven't already set a timeout, add one for every 5s.
                if self._send_typing_notification_timeout == 0:
                    self._send_typing_notification_timeout = \
                        gobject.timeout_add_seconds(5, self.send_typing_notification)

            else:
                # User is gone/inactive/active/paused, which basically means "not typing".
                # If we have a timeout for sending typing notifications, remove it.
                if self._send_typing_notification_timeout != 0:
                    gobject.source_remove(self._send_typing_notification_timeout)
                    self._send_typing_notification_timeout = 0



    def send_typing_notification(self):
        logger.debug('typing')

    @loggit(logger)
    def AcknowledgePendingMessages(self, ids):
        for id in ids:
            if id in self._pending_IM_messages:
                del self._pending_IM_messages[id]

        ChannelTypeText.AcknowledgePendingMessages(self, ids)

        self._conn.markAsRead(ids,self._handle.name)
        self.PendingMessagesRemoved(ids)

    @loggit(logger)
    def ListPendingMessages(self, clear):
        ret = ChannelTypeText.ListPendingMessages(self, clear)
        if clear:
            ids = self._pending_IM_messages.keys()
            self._pending_IM_messages = {}
            self.PendingMessagesRemoved(ids)

        return ret
