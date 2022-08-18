"""This topology for the Hello, CloudLab experiment includes two hosts
connected by a network link.

Instructions: Follow the instructions in [Hello, CloudLab](https://teaching-on-testbeds.github.io/hello-cloudlab/) 
to use this profile.
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

# Variable number of nodes.
pc.defineParameter("nodeCount", "Number of Nodes", portal.ParameterType.INTEGER, 1,
                   longDescription="If you specify more then one node, " +
                   "we will create a lan for you.")

# Pick your OS.
imageList = [
    ('default', 'Default Image'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD', 'UBUNTU 20.04'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD', 'UBUNTU 18.04'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//CENTOS7-64-STD',  'CENTOS 7'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//CENTOS8-64-STD',  'CENTOS 8'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//FBSD123-64-STD', 'FreeBSD 12.3'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//FBSD131-64-STD', 'FreeBSD 13.1')]

pc.defineParameter("osImage", "Select OS image",
                   portal.ParameterType.IMAGE,
                   imageList[0], imageList,
                   longDescription="Most clusters have this set of images, " +
                   "pick your favorite one.")

# Optional physical type for all nodes.
pc.defineParameter("phystype",  "Optional physical node type",
                   portal.ParameterType.STRING, "",
                   longDescription="Specify a physical node type (pc3000,d710,etc) " +
                   "instead of letting the resource mapper choose for you.")

# Optionally create XEN VMs instead of allocating bare metal nodes.
pc.defineParameter("useVMs",  "Use XEN VMs",
                   portal.ParameterType.BOOLEAN, False,
                   longDescription="Create XEN VMs instead of allocating bare metal nodes.")

# Optionally start X11 VNC server.
pc.defineParameter("startVNC",  "Start X11 VNC on your nodes",
                   portal.ParameterType.BOOLEAN, False,
                   longDescription="Start X11 VNC server on your nodes. There will be " +
                   "a menu option in the node context menu to start a browser based VNC " +
                   "client. Works really well, give it a try!")

# Optional link speed, normally the resource mapper will choose for you based on node availability
pc.defineParameter("linkSpeed", "Link Speed",portal.ParameterType.INTEGER, 0,
                   [(0,"Any"),(100000,"100Mb/s"),(1000000,"1Gb/s"),(10000000,"10Gb/s"),(25000000,"25Gb/s"),(100000000,"100Gb/s")],
                   advanced=True,
                   longDescription="A specific link speed to use for your lan. Normally the resource " +
                   "mapper will choose for you based on node availability and the optional physical type.")
                   
# For very large lans you might to tell the resource mapper to override the bandwidth constraints
# and treat it a "best-effort"
pc.defineParameter("bestEffort",  "Best Effort", portal.ParameterType.BOOLEAN, False,
                    advanced=True,
                    longDescription="For very large lans, you might get an error saying 'not enough bandwidth.' " +
                    "This options tells the resource mapper to ignore bandwidth and assume you know what you " +
                    "are doing, just give me the lan I ask for (if enough nodes are available).")
                    
# Sometimes you want all of nodes on the same switch, Note that this option can make it impossible
# for your experiment to map.
pc.defineParameter("sameSwitch",  "No Interswitch Links", portal.ParameterType.BOOLEAN, False,
                    advanced=True,
                    longDescription="Sometimes you want all the nodes connected to the same switch. " +
                    "This option will ask the resource mapper to do that, although it might make " +
                    "it imppossible to find a solution. Do not use this unless you are sure you need it!")

# Optional ephemeral blockstore
pc.defineParameter("tempFileSystemSize", "Temporary Filesystem Size",
                   portal.ParameterType.INTEGER, 0,advanced=True,
                   longDescription="The size in GB of a temporary file system to mount on each of your " +
                   "nodes. Temporary means that they are deleted when your experiment is terminated. " +
                   "The images provided by the system have small root partitions, so use this option " +
                   "if you expect you will need more space to build your software packages or store " +
                   "temporary files.")
                   
# Instead of a size, ask for all available space. 
pc.defineParameter("tempFileSystemMax",  "Temp Filesystem Max Space",
                    portal.ParameterType.BOOLEAN, False,
                    advanced=True,
                    longDescription="Instead of specifying a size for your temporary filesystem, " +
                    "check this box to allocate all available disk space. Leave the size above as zero.")

pc.defineParameter("tempFileSystemMount", "Temporary Filesystem Mount Point",
                   portal.ParameterType.STRING,"/mydata",advanced=True,
                   longDescription="Mount the temporary file system at this mount point; in general you " +
                   "you do not need to change this, but we provide the option just in case your software " +
                   "is finicky.")

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
iface_romeo.addAddress(rspec.IPv4Address("10.0.0.2", "255.255.255.0"))
lan_r.addInterface(iface_romeo)
node_romeo.startVNC()

# Set up first host - juliet
node_juliet = request.XenVM("juliet")
iface_juliet = node_juliet.addInterface("eth1")
iface_juliet.addAddress(rspec.IPv4Address("10.0.1.2", "255.255.255.0"))
lan_j.addInterface(iface_juliet)
node_juliet.startVNC()

# Set up router
node_router = request.XenVM("router")
iface_router_r = node_router.addInterface("eth1")
iface_router_r.addAddress(rspec.IPv4Address("10.0.0.1", "255.255.255.0"))
lan_r.addInterface(iface_router_r)
iface_router_j = node_router.addInterface("eth1")
iface_router_j.addAddress(rspec.IPv4Address("10.0.1.1", "255.255.255.0"))
lan_j.addInterface(iface_router_j)
node_router.startVNC()

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)