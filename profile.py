"""This topology has one host. Also, the `firefox` web browser is installed.

Spring 2024: modified by M. Toups to change hostname (more changes to come)

"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as rspec
# Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal context, needed to defined parameters
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Set up first host - romeo
node_greenwave_cloudlab = request.XenVM('greenwave-cloudlab')
node_greenwave_cloudlab.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD'
node_greenwave_cloudlab.addService(rspec.Execute(shell="bash", command="/usr/bin/sudo /usr/bin/apt purge firefox; /usr/bin/sudo /usr/bin/snap remove firefox; /usr/bin/sudo /usr/bin/add-apt-repository ppa:mozillateam/ppa -y ; /usr/bin/sudo /usr/bin/apt -y install firefox-esr; /usr/bin/sudo /usr/bin/ln -s /usr/bin/firefox-esr /usr/local/bin/firefox"))
node_greenwave_cloudlab.exclusive = False
node_greenwave_cloudlab.routable_control_ip = True # required for VNC
node_greenwave_cloudlab.startVNC()

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
