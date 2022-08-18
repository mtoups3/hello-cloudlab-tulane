"""This topology for the Hello, CloudLab experiment includes two hosts connected by a network link.

Follow the instructions in at https://teaching-on-testbeds.github.io/hello-cloudlab/ to use this profile.
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal context, needed to defined parameters
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Retrieve the values the user specifies during instantiation.
params = pc.bindParameters()

nodeCount = 3

pc.verifyParameters()

# Configure two links
lan_r = request.Link()
lan_r.best_effort = True

lan_j = request.Link()
lan_j.best_effort = True


# Set up first host - romeo
node_romeo = request.XenVM("romeo")
iface_romeo = node_romeo.addInterface("eth1")
iface_romeo.addAddress(pg.IPv4Address("10.0.0.2", "255.255.255.0"))
lan_r.addInterface(iface_romeo)
node_romeo.startVNC()

# Set up first host - juliet
node_juliet = request.XenVM("juliet")
iface_juliet = node_juliet.addInterface("eth1")
iface_juliet.addAddress(pg.IPv4Address("10.0.1.2", "255.255.255.0"))
lan_j.addInterface(iface_juliet)
node_juliet.startVNC()

# Set up router
node_router = request.XenVM("router")
iface_router_r = node_router.addInterface("eth1")
iface_router_r.addAddress(pg.IPv4Address("10.0.0.1", "255.255.255.0"))
lan_r.addInterface(iface_router_r)
iface_router_j = node_router.addInterface("eth2")
iface_router_j.addAddress(pg.IPv4Address("10.0.1.1", "255.255.255.0"))
lan_j.addInterface(iface_router_j)
node_router.startVNC()

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)