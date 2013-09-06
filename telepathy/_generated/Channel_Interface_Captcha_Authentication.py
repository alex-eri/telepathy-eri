# -*- coding: utf-8 -*-
# Generated from the Telepathy spec
""" Copyright © 2010-2012 Collabora Limited 

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
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
  
"""

import dbus.service


class ChannelInterfaceCaptchaAuthentication(dbus.service.Interface):
    """\
      A channel interface for captcha authentication.
        When this interface appears on a ServerAuthentication
        channel, it represents authentication with the server. In future,
        it could also be used to authenticate with secondary services,
        or even to authenticate end-to-end connections with contacts. As a result,
        this interface does not REQUIRE ServerAuthentication to allow for a potential future
        Channel.Type.PeerAuthentication interface.

      In any protocol that requires a captcha, the connection manager can
        use this channel to let a user interface carry out a simple captcha
        handshake with it, as a way to test the user is human
        interactively.

      For channels managed by a
        ChannelDispatcher,
        only the channel's Handler may call the
        methods on this interface. Other clients MAY observe the
        authentication process by watching its signals and properties.

      The most commonly used form of captcha challenge is OCR (recognition
        of distorted letters or words in an image), but for accessibility
        reasons, this interface also allows various other types of challenge,
        such as plain-text questions or recognition of words in audio. Its
        structure is modelled on XMPP's
        XEP-0158,
        but can be used with other protocols by mapping their semantics
        into those used in XMPP.

      
        It is important to support multiple types of captcha
          challenge to avoid discriminating against certain users; for
          instance, blind or partially-sighted users cannot be expected
          to answer an OCR challenge.

        XEP-0158 supports a superset of all other known protocols' captcha
          interfaces, and is sufficiently elaborate that we expect it will
          continue to do so.

        There can only be one Handler, which is a good fit for the
          question/answer model implied by captchas.
      
    """

    def __init__(self):
        self._interfaces.add('org.freedesktop.Telepathy.Channel.Interface.CaptchaAuthentication1')

    @dbus.service.method('org.freedesktop.Telepathy.Channel.Interface.CaptchaAuthentication1', in_signature='', out_signature='a(ussuas)us')
    def GetCaptchas(self):
        """
        Gets information regarding each of the captcha methods
          available and which and how many need to be successfully answered

        To call this method successfully, the state must be Local_Pending
          or Try_Again. If it is Local_Pending, it remains Local_Pending. If
          called more than once while in Local_Pending state, or if the state
          is Try_Again, this method fetches a new set of captcha challenges,
          if possible, and the state returns to Local_Pending.

        
          For instance, you could call GetCaptchas again from Local_Pending
            state if the user indicates that they can't understand the
            initially-offered captcha.

          This is a method, not a property, so that it can be used to
            fetch more than one set of captcha challenges, and so that
            change notification is not required. Only the Handler should
            call this method and calling GetAll would not reduce round-trips,
            so the usual reasons to prefer a property do not apply here.
        
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Channel.Interface.CaptchaAuthentication1', in_signature='us', out_signature='ay')
    def GetCaptchaData(self, ID, Mime_Type):
        """
        Fetch and return the captcha data. In protocols
          where captchas are downloaded out-of-band (for instance via HTTP),
          the connection manager is expected to do so.
        Returns an empty array if the type was "qa"
        
          If audio-based and image-based captchas are both available,
            we don't want to waste time downloading the audio until/unless
            the user asks to hear it. The extra D-Bus round-trips are not
            a problem, since they are expected to be quick compared with
            the time taken for the user to solve the captcha.
        
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Channel.Interface.CaptchaAuthentication1', in_signature='a{us}', out_signature='')
    def AnswerCaptchas(self, Answers):
        """
        Answer as many captchas as desired and/or required.
        Callable in state Local_Pending only. State changes to
          Remote_Pending.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Channel.Interface.CaptchaAuthentication1', in_signature='us', out_signature='')
    def CancelCaptcha(self, Reason, Debug_Message):
        """
        Cancel. State changes to Failed with error NotAvailable or
          Cancelled if it isn't already Failed. All you can do now is
          to close the channel.
      
        """
        raise NotImplementedError
  