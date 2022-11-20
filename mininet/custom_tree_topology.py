#
#   PROJECT : Mininet POX controller w/ OpenFlow
# 
#   FILENAME : ~/mininet/custom_tree_topology.py
# 
#   DESCRIPTION :
#   Use the NOX/POX controller platform for programming an OpenFlow-based SDN-enabled 
#   switch. The goal is to supply ow rules to the switch's ow table to implement a L2 
#   learning switching functionality.
# 
#   FUNCTIONS :
#       treeTopology()
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


"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def treeTopology():

    "Create an empty network and add nodes to it."

    # Set up the controller as a remote controller.
    net = Mininet( controller=RemoteController  , waitConnected=True )

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    # Endpoint devices.
    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip='10.0.0.1', mac='00:00:00:00:00:01' )
    h2 = net.addHost( 'h2', ip='10.0.0.2', mac='d0:13:1c:1b:76:a0' )
    h3 = net.addHost( 'h3', ip='10.0.0.3', mac='00:00:00:00:00:03' )
    h4 = net.addHost( 'h4', ip='10.0.0.4', mac='00:00:00:00:00:04' )
    h5 = net.addHost( 'h5', ip='10.0.0.5', mac='00:00:00:00:00:05' )
    h6 = net.addHost( 'h6', ip='10.0.0.6', mac='b8:94:91:62:f1:65' )

    # Switches
    info( '*** Adding switch\n' )
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )
    s3 = net.addSwitch( 's3' )
    s4 = net.addSwitch( 's4' )
    s5 = net.addSwitch( 's5' )
    s6 = net.addSwitch( 's6' )
    s7 = net.addSwitch( 's7' )

    # Since this is a tree topology, it's more scalable to define each layer.
    root = s1
    layer1 = [s2, s3]
    layer2 = [s4, s5, s6, s7]

    # Create links between endpoints and lowest layer of switches.
    info( '*** Creating links\n' )
    net.addLink( h1, s4 )
    net.addLink( h2, s4 )
    net.addLink( h3, s5 )
    net.addLink( h4, s6 )
    net.addLink( h5, s7 )
    net.addLink( h6, s7 )

    # Add links between each layer.
    for i, switchL1 in enumerate(layer1):
        net.addLink( root, switchL1 )
        net.addLink( switchL1, layer2[2 * i] )
        net.addLink( switchL1, layer2[2 * i + 1] )


    info( '*** Starting network\n')
    net.start()

    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    treeTopology()