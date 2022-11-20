#
#   PROJECT : Mininet POX controller w/ OpenFlow
# 
#   FILENAME : ~/pox/custom_l2_learning.py
# 
#   DESCRIPTION :
#   Use the NOX/POX controller platform for programming an OpenFlow-based SDN-enabled 
#   switch. The goal is to supply ow rules to the switch's ow table to implement a L2 
#   learning switching functionality.
# 
#   FUNCTIONS :
#       MyController.__init__()
#       MyController._handle_ConnectionUp()
#       L2Switch.__init__()
#       L2Switch._handle_PacketIn()
#       L2Switch.flood()
#       L2Switch.drop()
#       L2Switch.forward()
#       launch()
# 
#   NOTES :
#      - ...
# 
#   AUTHOR(S) : Noah Arcand Da Silva    START DATE : 2022.11.15 (YYYY.MM.DD)
#
#   CHANGES :
#       - ...
# 
#   VERSION     DATE        WHO             DETAILS
#   0.0.1a      2022.11.15  Noah            Creation of project.
#   0.0.1b      2022.11.17  Noah            Implementation of tree topolgy.
#   0.0.2a      2022.11.18  Noah            Full connectivity established.
#   0.0.2b      2022.11.19  Noah            Successful rule deployment.
#


from pox.core import core
from pox.openflow import libopenflow_01 as of
from pox.lib.addresses import EthAddr


class MyController(object):
    def __init__(self):
        core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        L2Switch(event.connection)


class L2Switch(object):
    def __init__(self, connection):
        print("L2 Switch")
        self.mactable = {}
        self.connection = connection
        connection.addListeners(self)

    def _handle_PacketIn(self, pkt_in_event):
        packet = pkt_in_event.parsed
        print(f"pkt: src {packet.src} dst {packet.dst} port {pkt_in_event.port}")
        
        # Setting mac addresses for rules:
        UNTRUSTED_MAC_ADDRESSES = [
            EthAddr('d0:13:1c:1b:76:a0'),
        ]
        PROTECTED_MAC_ADDRESSES = [
            EthAddr('b8:94:91:62:f1:65'),
        ]

        # Filling mac table for packet forwarding.
        self.mactable[packet.src] = pkt_in_event.port

        # First check for our rules.
        if (packet.src in UNTRUSTED_MAC_ADDRESSES) and (packet.dst in PROTECTED_MAC_ADDRESSES):
            print(f"Packet dropped. Untrusted source {packet.src} trying to reach protected host {packet.dst}")
            self.drop(pkt_in_event)
            return  # Prevent any further packet processing.

        # If the packet is not in the mac table.
        if packet.dst not in self.mactable:
             # Check if the packet is multicast.
            if packet.dst.is_multicast:
                print(f"Destination is multicast. Flooding.")
                self.flood(pkt_in_event)
            else:
                print(f"Port for {packet.dst} unknown. Flooding.")
                self.flood(pkt_in_event)
        # The packet is in the mac table,
        else:
            # Check if the destination port is the same as the input port.
            if self.mactable[packet.dst] == pkt_in_event.port:
                print(f"Packet from {packet.src} to {packet.dst} on {pkt_in_event.dpid}.{self.mactable[packet.dst]}" )
                self.drop(pkt_in_event) # Drop the packet to prevent looping.
                return  # Prevent any further packet processing.

            print(f"Forwarding {packet.src}.{pkt_in_event.port} to {packet.dst}.{self.mactable[packet.dst]}")
            self.forward(pkt_in_event, self.mactable[packet.dst])
    
    # Send packets to every port apart from the one which it entered.
    def flood(self, pkt_in_event):
        msg=of.ofp_packet_out()
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        msg.data=pkt_in_event.ofp
        msg.in_port=pkt_in_event.port
        self.connection.send(msg)

    # Drop the packet and prevent it from being processed any further.
    def drop(self, pkt_in_event):
        msg=of.ofp_packet_out()
        msg.data=pkt_in_event.ofp
        msg.in_port=pkt_in_event.port
        self.connection.send(msg)
    
    # Forward packet through specified port from mac table.
    def forward(self, pkt_in_event, to_port):
        packet=pkt_in_event.parse()
        msg=of.ofp_flow_mod()
        msg.match=of.ofp_match.from_packet(packet)
        msg.actions.append(of.ofp_action_output(port=to_port))
        msg.data=pkt_in_event.ofp
        #you can also set timeouts and priority
        self.connection.send(msg)


def launch():
    core.registerNew(MyController)