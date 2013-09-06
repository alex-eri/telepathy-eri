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


class CallStreamInterfaceMedia(dbus.service.Interface):
    """\
      This interface deals with how to connect a stream to an
      endpoint.  It contains all that is required to describe the
      local endpoint, to succesfully establish a connection. While a
      call is established, one may try to connect to multiple remote
      endpoints at the same time. This is called forking in the SIP
      jargon.  Informations related to the connections are on the
      Endpoint
      objects. Once the call is established, there MUST be a single
      endpoint left.

      ICE restarts

      If the CM wants to do an ICE restart, then the
        ICERestartPending property is set,
        and the ICERestartRequested signal is
        emitted. The streaming implementation should then call
        SetCredentials again. This will trigger
        the actual ICE restart, and cause
        LocalCandidates to be cleared.

      For more information on ICE restarts see
        RFC 5245
        section 9.1.1.1
    """

    def __init__(self):
        self._interfaces.add('org.freedesktop.Telepathy.Call1.Stream.Interface.Media')

    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', in_signature='u', out_signature='')
    def CompleteSendingStateChange(self, State):
        """
        Called in response to
          SendingStateChanged(Pending_*, *) to
          indicate that the media state has successfully progressed from
          Pending_{Start, Stop, Pause} to the corresponding non-pending
          state.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', in_signature='uss', out_signature='')
    def ReportSendingFailure(self, Reason, Error, Message):
        """
        Can be called at any point to indicate a failure in the outgoing
        portion of the stream.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', in_signature='u', out_signature='')
    def CompleteReceivingStateChange(self, State):
        """
        Called in response to
          ReceivingStateChanged(Pending_*, *) to
          indicate that the media state has successfully progressed from
          Pending_{Start, Stop, Pause} to the corresponding non-pending
          state.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', in_signature='uss', out_signature='')
    def ReportReceivingFailure(self, Reason, Error, Message):
        """
        Can be called at any point to indicate a failure in the incoming
        portion of the stream.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', in_signature='ss', out_signature='')
    def SetCredentials(self, Username, Password):
        """
        Used to set the username fragment and password for streams that have
          global credentials.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', in_signature='a(usua{sv})', out_signature='')
    def AddCandidates(self, Candidates):
        """
        Add candidates to the
        LocalCandidates property and
        signal them to the remote contact(s). Note that connection managers
        MAY delay the sending of candidates until
        FinishInitialCandidates is called.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', in_signature='', out_signature='')
    def FinishInitialCandidates(self):
        """
        This indicates to the CM that the initial batch of candidates
        has been added, and should now be processed/sent to the remote side.
        
          Protocols supporting Raw UDP SHOULD wait for FinishInitialCandidates,
          and then set the lowest priority candidate as the Raw UDP candidate.
        
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', in_signature='(uuss)', out_signature='')
    def Fail(self, Reason):
        """
        Signal an unrecoverable error for this stream, and remove it. If all
        streams are removed from a content, then it will also be removed.
      
        """
        raise NotImplementedError
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', signature='u')
    def SendingStateChanged(self, State):
        """
        Change notification for SendingState.
        Note that this information is duplicated onto the Stream interface, so
        that UIs can ignore the Media interface, and streaming implementations
        can ignore everything but the media interface.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', signature='u')
    def ReceivingStateChanged(self, State):
        """
        Change notification for ReceivingState.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', signature='a(usua{sv})')
    def LocalCandidatesAdded(self, Candidates):
        """
        Emitted when local candidates are added to the
        LocalCandidates property.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', signature='ss')
    def LocalCredentialsChanged(self, Username, Password):
        """
        Emitted when the value of
        LocalCredentials changes to a non-empty
        value. This should only happen when the streaming implementation calls
        SetCredentials, so this signal is
        mostly useful for debugging.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', signature='aa{sv}')
    def RelayInfoChanged(self, Relay_Info):
        """
        Emitted when the value of
        RelayInfo changes.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', signature='a(sq)')
    def STUNServersChanged(self, Servers):
        """
        Emitted when the value of
        STUNServers changes.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', signature='')
    def ServerInfoRetrieved(self):
        """
        Signals that the initial information about STUN and Relay servers
          has been retrieved, i.e. the
          HasServerInfo property is
          now true.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', signature='aoao')
    def EndpointsChanged(self, Endpoints_Added, Endpoints_Removed):
        """
        Emitted when the Endpoints property
        changes.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream.Interface.Media', signature='')
    def ICERestartRequested(self):
        """
        Emitted when the remote side requests an ICE restart (e.g. third party
        call control, when the remote endpoint changes). The streaming
        implementation should call
        SetCredentials again.
      
        """
        pass
  