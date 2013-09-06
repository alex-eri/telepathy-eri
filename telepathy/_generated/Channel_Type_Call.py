# -*- coding: utf-8 -*-
# Generated from the Telepathy spec
"""Copyright © 2009-2010 Collabora Limited
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
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
  
"""

import dbus.service


class ChannelTypeCall(dbus.service.Interface):
    """\
      A channel type for making audio and video calls. Call
        channels supersede the old StreamedMedia
        channel type. Call channels are much more flexible than its
        predecessor and allow more than two participants.

      Handlers are advised against executing all the media
        signalling, codec and candidate negotiation themselves but
        instead use a helper library such as telepathy-farstream
        which when given a new Call channel will set up the
        transports and codecs and create GStreamer pads which
        can be added to the handler UI. This is useful as it means
        the handler does not have to worry how exactly the
        connection between the call participants is being made.

      The TargetHandle and
        TargetID
        properties in a Call channel refer to the contact that the
        user initially called, or which contact initially called the
        user. Even in a conference call, where there are multiple
        contacts in the call, these properties refer to the
        initial contact, who might have left the conference since
        then. As a result, handlers should not rely on these
        properties.

      Contents

      Content
        objects represent the actual media that forms the Call (for
        example an audio content and a video content). Calls always
        have one or more Content objects associated with them. As a
        result, a new Call channel request MUST have either
        InitialAudio=True, or
        InitialVideo=True, or both,
        as the Requestable Channel Classes will document.

      Content objects have
        one or more stream associated with them. More information on
        these streams and how to maniuplate them can be found on the
        Content
        interface page.

      Outgoing calls

      To make an audio-only call to a contact foo@example.com
        handlers should call:

      
        
CreateChannel({
  ...ChannelType: ...Call1,
  ...TargetHandleType: Contact,
  ...TargetID: 'foo@example.com',
  ...InitialAudio: True,
})

      As always, TargetHandle may be used
        in place of
        TargetID
        if the contact's handle is already known. To make an audio
        and video call, the handler should also specify
        InitialVideo The
        connection manager SHOULD return a channel whose immutable
        properties contain the local user as the InitiatorHandle, the
        remote contact as the TargetHandle,
        Requested =
        True (indicating the call is outgoing).

      After a new Call channel is requested, the
        CallState property will be
        Pending_Initiator. As the local
        user is the initiator, the call must be accepted by the handler
        by calling the Accept method.
        At this point, CallState changes
        to Initialising, which signifies
        that the call is waiting for the network to do
        something. When the CM has information indicating that the remote contact has been
        notified about the call (or immediately if the network is known not to convey such
        information) it should also change to
        Initialised. All changes to
        the CallState property are signalled using
        the CallStateChanged signal.

      When the call is accepted by the remote contact, the
        CallStateChanged signal fires
        again to show that CallState =
        Accepted.

      At this point telepathy-farstream
        will signal that a pad is available for the handler to show
        in the user interface. Once media is correctly flowing in both
        directions, the state will change to
        Active, to inform the user that they
        have a correctly working call there is nothing amiss.

      Missed calls

      If the remote contact does not accept the call in time, then
        the call can be terminated by the server. Note that this only
        happens in some protocols. Most XMPP clients, for example, do
        not do this and rely on the call initiator terminating the call.
        A missed call is shown in a Call channel by the
        CallState property changing to
        Ended, and the
        CallStateReason property changing
        to (remote contact,
        No_Answer, "").

      Rejected calls

      If the remote contact decides he or she does not feel like
        talking to the local user, he or she can reject his or her
        incoming call. This will be shown in the Call channel by
        CallState changing to
        Ended and the
        CallStateReason property
        changing to (remote contact,
        User_Requested,
        "org.freedesktop.Telepathy.Error.Rejected").

      Incoming calls

      When an incoming call occurs, something like the following
        NewChannels
        signal will occur:

      
        
NewChannels([
  /org/freedesktop/Telepathy/Connection/foo/bar/foo_40bar_2ecom/CallChannel,
  {
    ...ChannelType: ...Call1,
    ...TargetHandleType: Contact,
    ...TargetID: 'foo@example.com',
    ...TargetHandle: 42,
    ...Requested: False,
    ...InitialAudio: True,
    ...InitialVideo: True,
    ...InitialAudioName: "audio",
    ...InitialVideoName: "video",
    ...MutableContents: True,
  }])

      The InitialAudio and
        InitialVideo properties show that
        the call has been started with two contents: one for audio
        streaming and one for video streaming. The
        InitialAudioName and
        InitialVideoName properties also
        show that the aforementioned audio and video contents have names
        "audio" and "video".

      Once the handler has notified the local user that there is an
        incoming call waiting for acceptance, the handler should call
        SetRinging to let the CM know.
        The new channel should also be given to telepathy-farstream to
        work out how the two participants will connect together.
        telepathy-farstream will call the appropriate methods on the call's
        Contents
        to negotiate codecs and transports.

      To pick up the call, the handler should call
        Accept. The
        CallState property changes to
        Accepted and once media is
        being transferred, telepathy-farstream will notify the
        handler of a new pad to be shown to the local user in the
        UI. Once media is correctly flowing in both directions, the state will
        change to Active, to inform the user
        that they have a correctly working call there is nothing amiss.

      To reject the call, the handler should call the
        Hangup method. The
        CallState property will change to
        Ended and the
        CallStateReason property will
        change to (self handle,
        User_Requested,
        "org.freedesktop.Telepathy.Error.Rejected").

      Ongoing calls

      Adding and removing contents

      When a call is open, new contents can be added as long as the
        CM supports it. The
        MutableContents property will let
        the handler know whether further contents can be added or
        existing contents removed. An example of this is starting a
        voice call between a contact and then adding a video content.
        To do this, the should call
        AddContent like this:

      
        AddContent("video",
           Video)
      

      Assuming no errors, the new video content will be added to
        the call. telepathy-farstream will pick up the new content and
        perform the transport and codec negotiation automatically.
        telpathy-farstream will signal when the video is ready to
        show in the handler's user interface.

      A similar method is used for removing contents from a call,
        except that the Remove method
        is on the Content object.

      Ending the call

      To end the call, the handler should call the
        Hangup method. The
        CallState property will change to
        Ended and
        CallStateReason will change
        to (self handle,
        User_Requested,
        "org.freedesktop.Telepathy.Error.Cancelled").

      If the other participant hangs up first then the
        CallState property will change to
        Ended and
        CallStateReason will change
        to (remote contact,
        User_Requested,
        "org.freedesktop.Telepathy.Error.Terminated").

      Multi-party calls

      Requestable channel classes

      The RequestableChannelClasses
        for Call1 channels
        can be:

      
        
[( Fixed = { ...ChannelType: ...Call1,
            ...TargetHandleType: Contact,
            ...InitialVideo: True
          },
  Allowed = [ ...InitialVideoName,
              ...InitialAudio,
              ...InitialAudioName
            ]
),
( Fixed = { ...ChannelType: ...Call1,
            ...TargetHandleType: Contact,
            ...InitialAudio: True
          },
  Allowed = [ ...InitialAudioName,
              ...InitialVideo,
              ...InitialVideoName
            ]
)]

      Clients aren't allowed to make outgoing calls that have
        neither initial audio nor initial video. Clearly, CMs
        which don't support video should leave out the first class and
        omit InitialVideo from the second
        class, and vice versa for CMs without audio support.

      Handlers should not close Call1 channels
        without first calling Hangup on
        the channel. If a Call handler crashes, the ChannelDispatcher will call
        Close on the
        channel which SHOULD also imply a call to
        Hangup(User_Requested,
        "org.freedesktop.Telepathy.Error.Terminated", "") before
        actually closing the channel.

    """

    @dbus.service.method('org.freedesktop.Telepathy.Channel.Type.Call1', in_signature='', out_signature='')
    def SetRinging(self):
        """
        Indicate that the local user has been alerted about the incoming
          call.

        This method is only useful if the
          channel's Requested
          property is False, and
          the CallState is
          Initialised (an incoming
          call is ready and waiting for the user to be notified). Calling this method
          SHOULD set CallFlags' bit
          Locally_Ringing, and notify the
          remote contact that the local user has been alerted (if the
          protocol supports this); repeated calls to this method
          SHOULD succeed, but have no further effect.

        In all other states, this method SHOULD fail with the error
          NotAvailable.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Channel.Type.Call1', in_signature='', out_signature='')
    def SetQueued(self):
        """
        Notifies the CM that the local user is already in a call, so this
          call has been put in a call-waiting style queue.

        This method is only useful if the
          channel's Requested
          property is False, and
          the CallState is
          Initialising or
          Initialised. Calling this method
          SHOULD set CallFlags' bit
          Locally_Queued, and notify the
          remote contact that the call is in a queue (if the
          protocol supports this); repeated calls to this method
          SHOULD succeed, but have no further effect.

        Locally_Queued is a little like Locally_Held, but applies to calls that have not
          been Accepted (the Locally_Queued flag should be unset by the CM when Accept
          is called). It should also be set in response to the state of the
          world, rather than in response to user action.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Channel.Type.Call1', in_signature='', out_signature='')
    def Accept(self):
        """
        For incoming calls in state
          Initialised, accept the incoming call.
          This changes the CallState to
          Accepted.

        For outgoing calls in state
          Pending_Initiator, actually
          call the remote contact; this changes the
          CallState to
          Initialising.

        Otherwise, this method SHOULD fail with the error NotAvailable.

        This method should be called exactly once per Call, by whatever
          client (user interface) is handling the channel.

        When this method is called, for each Content whose
          Disposition is
          Initial, any
          streams where the LocalSendingState
          is Pending_Send will be
          moved to Sending as if
          SetSending(True) had been called.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Channel.Type.Call1', in_signature='uss', out_signature='')
    def Hangup(self, Reason, Detailed_Hangup_Reason, Message):
        """
        Request that the call is ended. All contents will be removed
        from the Call so that the
        Contents property will be the
        empty list.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Channel.Type.Call1', in_signature='suu', out_signature='o')
    def AddContent(self, Content_Name, Content_Type, InitialDirection):
        """
        Request that a new Content of type
        Content_Type is added to the Call1. Handlers should check the
        value of the MutableContents
        property before trying to add another content as it might not
        be allowed.
      
        """
        raise NotImplementedError
  
    @dbus.service.signal('org.freedesktop.Telepathy.Channel.Type.Call1', signature='o')
    def ContentAdded(self, Content):
        """
        Emitted when a new Content is added to the call.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Channel.Type.Call1', signature='o(uuss)')
    def ContentRemoved(self, Content, Reason):
        """
        Emitted when a Content is removed from the call.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Channel.Type.Call1', signature='uu(uuss)a{sv}')
    def CallStateChanged(self, Call_State, Call_Flags, Call_State_Reason, Call_State_Details):
        """
        Emitted when the state of the call as a whole changes.

        This signal is emitted for any change in the properties
          corresponding to its arguments, even if the other properties
          referenced remain unchanged.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Channel.Type.Call1', signature='a{uu}a{us}au(uuss)')
    def CallMembersChanged(self, Flags_Changed, Identifiers, Removed, Reason):
        """
        Emitted when the CallMembers property
        changes in any way, either because contacts have been added to the
        call, contacts have been removed from the call, or contacts' flags
        have changed.
      
        """
        pass
  