# -*- coding: utf-8 -*-
# Generated from the Telepathy spec
"""Copyright © 2009-2010 Collabora Ltd.
Copyright © 2009-2010 Nokia Corporation

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


class CallContentInterfaceMedia(dbus.service.Interface):
    """\
      Interface to use by a software implementation of media
        streaming. The reason behind splitting the members of this
        interface out from the main Content interface is
        that the software is not necessarily what controls the
        media. An example of this is in GSM phones, where the CM just
        tells the phone to dial a number and it does the audio routing
        in a device specific hardware way and the CM does not need
        to concern itself with codecs.

      Codec Negotiation

      When a new Call1 channel
        appears (whether it was requested or not) a MediaDescription
        object will either be waiting in the
        MediaDescriptionOffer property, or will
        appear at some point via the
        NewMediaDescriptionOffer signal.

      If nothing is known about the remote side's Media capabilities
        (e.g. outgoing SIP/XMPP call), this MediaDescription will pop up with {HasRemoteInformation = false, FurtherNegotiationRequired = true}, and the local
        user's streaming implementation SHOULD call 
        Accept,
        with a description of all supported codecs and other features.
        The CM will then send this information to the remote side (and
        LocalMediaDescriptionChanged will fire
        with details of the description passed into Accept for debugging purposes).
      
      When the remote codecs and other content information are available
        (e.g. Remote user replies to initial offer, or sends a new offer of
        their own, a new MediaDescription will appear, with {HasRemoteInformation = true, FurtherNegotiationRequired = false},
        and the Codecs
        property on the description offer set to the codecs which are
        supported by the remote contact. The local user's streaming
        implementation SHOULD then call Accept, with a description
        that is compatible with the one one in the offer. After the codec
        set is accepted, both
         LocalMediaDescriptionChanged and
         RemoteMediaDescriptionsChanged
        will fire to signal their respective changes, to aid with debugging.
        Note that if Accept is called, with FurtherNegotiationRequired set to false,
        the CM should be able to rely on the fact that the
        description passed into Accept is compatible with the one in the
        offer, and the description passed into Accept will not be signalled to
        the remote side.
      

      Changing codecs mid-call

      To update the codecs in the local (and optionally remote) media
        descriptions mid-call, the
        UpdateLocalMediaDescription method
        should be called with details of the new codec list. If this is
        accepted, then
        LocalMediaDescriptionChanged
        will be emitted with the new codec set.
      
       If parameters requiring negotiation are changed, then the
        FurtherNegotiationRequired property should be set to
        TRUE, and the new media description should
        only be used once they come in a new MediaDescriptionOffer
      

      If the other side decides to update his or her codec list
        during a call, a new MediaDescription
        object will appear through
        NewMediaDescriptionOffer which should be
        acted on as documented above.

      Protocols without negotiation

      For protocols where the codecs are not negotiable, the initial content's MediaDescription
        object will appear with HasRemoteInformation,
        set to true and the known supported codec values in Codecs.
      
    """

    def __init__(self):
        self._interfaces.add('org.freedesktop.Telepathy.Call1.Content.Interface.Media')

    @dbus.service.method('org.freedesktop.Telepathy.Call1.Content.Interface.Media', in_signature='a{sv}', out_signature='')
    def UpdateLocalMediaDescription(self, MediaDescription):
        """
        Update the local codec mapping and other interfaces of the
        MediaDescription. This method should only be
        used during an existing call to update the local media description.
        This may trigger a re-negotiation which may result in new
        new MediaDescriptionOffers if the "FurtherNegotiationRequired"
        property is TRUE.
        Otherwise, only parameters which strictly describe the media being sent
        can be changed.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Content.Interface.Media', in_signature='yu', out_signature='')
    def AcknowledgeDTMFChange(self, Event, State):
        """
        Called by the streaming implementation in response to
        DTMFChangeRequested to confirm that it
        has started or stopped sending the event in question.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Content.Interface.Media', in_signature='(uuss)', out_signature='')
    def Fail(self, Reason):
        """
        Signal an unrecoverable error for this content, and remove it.
      
        """
        raise NotImplementedError
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Content.Interface.Media', signature='oa{sv}')
    def NewMediaDescriptionOffer(self, Media_Description, Properties):
        """
        Emitted when a new MediaDescription appears. The streaming
          >implementation MUST respond by calling the
          Accept or Reject method on the description object appeared.

        Emission of this signal indicates that the
          MediaDescriptionOffer property has
          changed to
            (Description, Contact, MediaDescriptionProperties).

        When the MediaDescriptionOffer has been dealt with then
          MediaDescriptionOfferDone must be emitted
          before NewMediaDescriptionOffer is emitted again.
        

      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Content.Interface.Media', signature='')
    def MediaDescriptionOfferDone(self):
        """
        Emitted when a MediaDescription has been handled. 
        Emission of this signal indicates that the
          MediaDescriptionOffer property has
          changed to
            ("/", 0, {}).
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Content.Interface.Media', signature='a{sv}')
    def LocalMediaDescriptionChanged(self, Updated_Media_Description):
        """
        Change notification for
            LocalMediaDescriptions
        
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Content.Interface.Media', signature='a{ua{sv}}')
    def RemoteMediaDescriptionsChanged(self, Updated_Media_Descriptions):
        """
        Change notification for
            RemoteMediaDescriptions
        
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Content.Interface.Media', signature='au')
    def MediaDescriptionsRemoved(self, Removed_Media_Descriptions):
        """
        Removal notification for
            RemoteMediaDescriptions
            and
            LocalMediaDescriptions
        
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Content.Interface.Media', signature='yu')
    def DTMFChangeRequested(self, Event, State):
        """
        Used by the CM to relay instructions from Channel.Interface.DTMF to the streaming
        implementation. If any contact in this call supports the
        telephone-event codec in their MediaDescription, this event should be
        sent as outlined in RFC 4733. Otherwise, it should be sent as an
        audible tone.
      
        """
        pass
  