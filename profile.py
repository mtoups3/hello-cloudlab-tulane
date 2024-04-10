"""This topology has one host, to allow students to test using CloudLab experiments.

Spring 2024: updated by M. Toups
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

# Set up first host - greenwave-cloudlab (foremerly romeo)
node_greenwave_cloudlab = request.XenVM('greenwave-cloudlab')
node_greenwave_cloudlab.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD'

# comment out below - we don't need firefox anymore
#node_greenwave_cloudlab.addService(rspec.Execute(shell="bash", command="/usr/bin/sudo /usr/bin/apt purge firefox; /usr/bin/sudo /usr/bin/snap remove firefox; /usr/bin/sudo /usr/bin/add-apt-repository ppa:mozillateam/ppa -y ; /usr/bin/sudo /usr/bin/apt -y install firefox-esr; /usr/bin/sudo /usr/bin/ln -s /usr/bin/firefox-esr /usr/local/bin/firefox"))
# commands below replace MOTD with Tulane specific stuff --mt
node_greenwave_cloudlab.addService(rspec.Execute(shell="bash", command='/usr/bin/sudo /bin/rm /etc/update-motd.d/*')) # remove default Ubuntu stuff
node_greenwave_cloudlab.addService(rspec.Execute(shell="bash",command='/usr/bin/sudo /usr/bin/wget -O /etc/profile.d/00tulane-profile.sh https://raw.githubusercontent.com/mtoups3/hello-cloudlab-tulane/main/00tulane-profile.sh'))
node_greenwave_cloudlab.addService(rspec.Execute(shell="bash", command='/usr/bin/sudo /usr/bin/chmod +x /etc/profile.d/00tulane-profile.sh'))
# get rid of annoying ubuntu legal stuff
node_greenwave_cloudlab.addService(rspec.Execute(shell="bash",command='/usr/bin/sudo rm /etc/legal'))

node_greenwave_cloudlab.exclusive = False # use False for shared Xen VMs

### disabling VNC to try to make this easier to start up on Cloudlab
#node_greenwave_cloudlab.routable_control_ip = True # required for VNC
#node_greenwave_cloudlab.startVNC()

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
