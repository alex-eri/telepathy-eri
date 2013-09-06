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


class CallStreamEndpoint(dbus.service.Object):
    """\
      This object represents an endpoint for a stream. In a one-to-one
        call, there will be one (bidirectional) stream per content and
        one endpoint per stream (as there is only one remote
        contact). In a multi-user call there is a stream for each remote
        contact and each stream has one endpoint as it refers to the one
        physical machine on the other end of the stream.

      The multiple endpoint use case appears when SIP call forking
        is used. Unlike jingle call forking (which is just making
        multiple jingle calls to different resources appear as one
        call), SIP call forking is actually done at the server so you
        have one stream to the remote contact and then and endpoint for
        each SIP client to be called.
    """

    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream.Endpoint', in_signature='(usua{sv})(usua{sv})', out_signature='')
    def SetSelectedCandidatePair(self, Local_Candidate, Remote_Candidate):
        """
        Update the entry in
        SelectedCandidatePairs
        for a particular component, and signal it to the remote side.

        This method should only be called by the controlling side of an
        ICE session. See CandidatePairSelected
        for details.

        
          In the SDP offer/answer model, this signalling will take place as
          generating an updated offer.
          Note that updates may be queued up until information about all
          components of all streams is gathered.
        
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream.Endpoint', in_signature='uu', out_signature='')
    def SetEndpointState(self, Component, State):
        """
        Change the EndpointState of the
        endpoint.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream.Endpoint', in_signature='(usua{sv})(usua{sv})', out_signature='')
    def AcceptSelectedCandidatePair(self, Local_Candidate, Remote_Candidate):
        """
        Called in response to
        CandidatePairSelected if/when this
        candidate pair is known to have passed its connectivity checks.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream.Endpoint', in_signature='(usua{sv})(usua{sv})', out_signature='')
    def RejectSelectedCandidatePair(self, Local_Candidate, Remote_Candidate):
        """
        Called in response to
        CandidatePairSelected if/when this
        candidate pair is known to have failed its connectivity checks.
      
        """
        raise NotImplementedError
  
    @dbus.service.method('org.freedesktop.Telepathy.Call1.Stream.Endpoint', in_signature='b', out_signature='')
    def SetControlling(self, Controlling):
        """
        Set whether the local side is taking the Controlling role. Note that
        if there are multiple endpoints (e.g. SIP call forking) it may be the
        case that all endpoints need to have the same controlling/controlled
        orientation.
      
        """
        raise NotImplementedError
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream.Endpoint', signature='ss')
    def RemoteCredentialsSet(self, Username, Password):
        """
        Emitted when the remote ICE credentials for the endpoint are
        set. If each candidate has different credentials, then this
        signal will never be fired.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream.Endpoint', signature='a(usua{sv})')
    def RemoteCandidatesAdded(self, Candidates):
        """
        Emitted when remote candidates are added to the
        RemoteCandidates property.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream.Endpoint', signature='(usua{sv})(usua{sv})')
    def CandidatePairSelected(self, Local_Candidate, Remote_Candidate):
        """
        Emitted when a candidate is selected for use in the stream by the
        controlling side of an ICE session.
        The controlled side should call
        AcceptSelectedCandidatePair or
        RejectSelectedCandidatePair when
        connectivity checks have either succeeded or failed for this candidate
        pair. See also: SelectedCandidatePairs.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream.Endpoint', signature='uu')
    def EndpointStateChanged(self, Component, State):
        """
        Emitted when the EndpointState
        property changes.
      
        """
        pass
  
    @dbus.service.signal('org.freedesktop.Telepathy.Call1.Stream.Endpoint', signature='b')
    def ControllingChanged(self, Controlling):
        """
        The value of Controlling has changed.
      
        """
        pass
  