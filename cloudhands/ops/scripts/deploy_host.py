#!/usr/bin/env python
# encoding: UTF-8

import socket
import sys
import subprocess
import getpass
import time
import re
import os
import time
import shutil
import subprocess

import cloudhands.ops.scripts.parse_yaml as plat
import cloudhands.ops.scripts.maintain_routes as maintain_routes

identity=sys.argv[1]
hostNum = str(sys.argv[2])
dhcpConf = "/etc/dhcp/dhcpd.conf"
tmpDhcpConf = "/tmp/dhcpd-working.conf"
date=time.strftime("%Y%m%d%H%M%S")
ipmiConStr = plat.GetIpmi()

(""" This script handles the entire deployment process as documented in the STFC svn repository. The script automates the process managing the DHCP configuration, IPMI configuration, vSphere configuration and vCloud registration. 

Each specific task has been handled with its own comment meaning that changes to the manual process can be easily mapped and altered within this code
""")

def CheckSyntax():
	(""" This function checks the syntax of the arguments passed to the script. If they are incorrect it prints the correct usage tot he screen.
""")
	if sys.argv is None or len(sys.argv) <= 2:
		print("\nThis script is used to manage the deployment and decomissiong of ESXi hosts for the Jasmin 2 vCloud infastructure.\n\nPlease run " + sys.argv[0] + " <build|decom> <host number>\n")
		exit(1)
	if identity.lower() == "build" or identity.lower() == "decom" or identity.lower() == "debug":
		return
	else:
		print("Please state whether the host should be built or decomissioned")
		exit(1)

def testDhcp(server, key):
	(""" This code makes a remote SSH call tot eh DHCP server and runs a syntax check against the DHCP configuration file. This is used to validate the configuration before restarting the DHCP service.
""")
	if plat.ExecSshCommand(server, key, "/usr/sbin/dhcpd -t -cf " + dhcpConf)[1] != 0:
                print("The current DHCP configuration would not load successfully. No changes will be made. Please resolve this issue before running this script.")

def backupDhcp(server, key):
	(""" This method makes a remote SSH call to backup the current DHCP configuration with a date and time stamp before any configuration alterations are made allowing for easy restoration. The filename is printed tot he screen to allow the administrator to easily rollback changes in the event something goes very wrong!
""")
	if plat.ExecSshCommand(server, key, "cp " + dhcpConf + " " + dhcpConf + ".backup." + date)[1] != 0:
		print("Failed to backup the current DHCP configuration. This script will exit without making any changes")
	else:
		print("Backuped up the DHCP config on " + server + " to " + dhcpConf + ".backup." + date + ".")

def commentInHost():
	(""" This code works on a local copy of the DHCP configuration to make the neccessary changes to comment in a host. The code is responsible for allowing the server to recieve a DHCP address without a PXE imagine meaning it will eventually boot from the OS installed on the disk.
""")

	pattern = "#.*(host vjasmin-vesx)" + hostNum + "(.jc.rl.ac.uk {)\n#.*(hardware.*)\n#.*(fixed.*)\n#.*(}.*)\n"
	patterna = "#.*(host vjasmin-vesxb)" + hostNum + "(.jc.rl.ac.uk {)\n#.*(hardware.*)\n#.*(fixed.*)\n#.*(}.*)\n"
	try:
		data = open(tmpDhcpConf, "r+")
		config=re.sub(pattern, "\t\g<1>" + hostNum + "\g<2>\n\t\t\g<3>\n\t\t\g<4>\n\t\g<5>\n", data.read(), re.MULTILINE)
		config=re.sub(patterna, "\t\g<1>" + hostNum + "\g<2>\n\t\t\g<3>\n\t\t\g<4>\n\t\g<5>\n", config, re.MULTILINE)
		data.close
		data = open(tmpDhcpConf, "w+")
		data.write(config)
	except ValueError:
		print ( "failed to edit " + tmpDhcpConf )

def commentOutHost():
	("""This code works on a local copy of the DHCP configuration to make the neccessary changes to comment out a host. By doing this it prevents the server getting a DHCP address from the DHCP server used by autodeploy. This means the server can pick up an address from the current STFC DHCP used to run kickstart.
""")
	pattern = "(.*host vjasmin-vesx)" + hostNum + "(.jc.rl.ac.uk {)\n(.*)\n(.*)\n(.*)\n"
	patterna = "(.*host vjasmin-vesxb)" + hostNum + "(.jc.rl.ac.uk {)\n(.*)\n(.*)\n(.*)\n"
	try:
		data = open(tmpDhcpConf, "r+")
		config=re.sub(pattern, "#\g<1>" + hostNum + "\g<2>\n#\g<3>\n#\g<4>\n#\g<5>\n", data.read(), re.MULTILINE)
		config=re.sub(patterna, "#\g<1>" + hostNum + "\g<2>\n#\g<3>\n#\g<4>\n#\g<5>\n", config, re.MULTILINE)
		data.close
		data = open(tmpDhcpConf, "w+")
		data.write(config)
	except ValueError:
		print ( "failed to edit " + tmpDhcpConf )

def commentInBootImage():
	(""" This code works on a local copy of the DHCP configuration to make the neccessary changes to comment in a host. The code is responsible injecting the PXE boot file into the DHCP configuration meaning the server will be rebuilt OVERWRITTING any OS installed on the disk!
""")
	pattern = "(.*)host vjasmin-vesx" + hostNum + ".jc.rl.ac.uk {\n(.*)hardware"
	patterna = "(.*)host vjasmin-vesxb" + hostNum + ".jc.rl.ac.uk {\n(.*)hardware"
	try:
		data = open(tmpDhcpConf, "r+")
		config=re.sub(pattern, "\thost vjasmin-vesx" + hostNum + ".jc.rl.ac.uk {\n\t\tfilename \"undionly.kpxe.vmw-hardwired\";\n\t\thardware", data.read(), re.MULTILINE)
		config=re.sub(patterna, "\thost vjasmin-vesxb" + hostNum + ".jc.rl.ac.uk {\n\t\tfilename \"undionly.kpxe.vmw-hardwired\";\n\t\thardware", config, re.MULTILINE)
		data.close
		data = open(tmpDhcpConf, "w+")
		data.write(config)
	except ValueError:
		print ( "failed to edit " + tmpDhcpConf )

def commentOutBootImage():
	(""" This code works on a local copy of the DHCP configuration to make the neccessary changes to comment in a host. The code is responsible for removing the boot file meaning hte server will eventually boot from the OS image installed ont he disk.
""")
	pattern = "(.*)host vjasmin-vesx" + hostNum + ".jc.rl.ac.uk {\n(.*)filename(.*)\n"
	patterna = "(.*)host vjasmin-vesxb" + hostNum + ".jc.rl.ac.uk {\n(.*)filename(.*)\n"
	try:
		data = open(tmpDhcpConf, "r+")
		config=re.sub(pattern, "\thost vjasmin-vesx" + hostNum + ".jc.rl.ac.uk {\n", data.read(), re.MULTILINE)
		config=re.sub(patterna, "\thost vjasmin-vesxb" + hostNum + ".jc.rl.ac.uk {\n", config, re.MULTILINE)
		data.close
		data = open(tmpDhcpConf, "w+")
		data.write(config)
	except ValueError:
		print ( "failed to edit " + tmpDhcpConf )

def copyDhcpConfig(server, key):
    (""" This SCPs a copy of the DHCP config from the DHCP server used by autodeploy. This is the local copy manipulated by the commenting funcitons above.
""")
    result = subprocess.Popen([
        'scp', "-i", key,
        server + ":" + dhcpConf, tmpDhcpConf],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    streamdata = result.communicate()
    rc = result.returncode
    stdout = streamdata

def uploadDhcpConfig(server, key):
    (""" This SCPs a copy of the modifed DHCP config from the local server to the DHCP server used by autodeploy. 
""")
    result = subprocess.Popen([
        'scp', "-i", key,
        tmpDhcpConf, server + ":" + dhcpConf],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    streamdata = result.communicate()
    rc = result.returncode
    stdout = streamdata

def restartDhcp(server, key):
	(""" This code makes a remote SSH call to restart DHCP on the DHCP server used by autodeploy. """)
	plat.ExecSshCommand(server, key, "service dhcpd restart")

def setPXE():
	(""" This code tells the host to PXE boot via IPMI. This is to protect against assuming the host is set to boot via PXE. """)
	subprocess.call(["ipmitool", "-H", ipmiConStr.Name + hostNum + ipmiConStr.Domain, "-I", "lanplus", "-U", ipmiConStr.Username, "-P", ipmiConStr.Password, "chassis",  "bootdev", "pxe"])

def RebootHost():
	(""" This reboots the host via IPMI. It specifically stops and starts the host as using the reset option proved to be buggy.""")
	subprocess.call(["ipmitool", "-H", ipmiConStr.Name + hostNum + ipmiConStr.Domain, "-I", "lanplus", "-U", ipmiConStr.Username, "-P", ipmiConStr.Password, "chassis", "power", "reset"])
	time.sleep(5)
	status=0
	while status != 1:
                status=subprocess.Popen(["ipmitool", "-H", ipmiConStr.Name + hostNum + ipmiConStr.Domain, "-U", ipmiConStr.Username, "-P", ipmiConStr.Password, "power", "status"],stdout=subprocess.PIPE).stdout.read()
                if "Chassis Power is on" in str(status):
                        status=1
                print("powering on host...")
                subprocess.call(["ipmitool", "-H", ipmiConStr.Name + hostNum + ipmiConStr.Domain, "-I", "lanplus", "-U", ipmiConStr.Username, "-P", ipmiConStr.Password, "chassis", "power", "on"])
                time.sleep(5)

def getIqn():
	(""" This returns the IQN from the host to allow addition or removal from the storage IQN groups. """)
	data = str(plat.ExecCommand(hostNum, "iscsi adapter list"))
	return str(re.match(".*(iqn.1998-01.com.vmware:.*)  iSCSI .*", data).group(1))

def checkMaint():
	(""" Tests whether the host is in maintenance mode """)
	state = str(plat.ExecCommand(hostNum, "system maintenanceMode get"))
	if re.match(r".*Enabled.*", state):
		time.sleep(10)
		checkMaint()
	else:
		(""" We pause here for 30 seconds to allow vShiled manager to add the VXLAN virtual NIC """)
		time.sleep(30)
		return "Host has left maintenance mode"

def enterMaint():
	plat.ExecCommand(hostNum, "system maintenanceMode set -e true")

def exitMaint():
	plat.ExecCommand(hostNum, "system maintenanceMode set -e false")

def esxReboot():
	plat.ExecCommand(hostNum, "system shutdown reboot --reason=Rebooting to apply iSCSI routes")

def checkServerAvail():
	state = str(plat.ExecCommand(hostNum, "system maintenanceMode get"))
	if re.match(r".*Cannot find ESX host.*", state):
		time.sleep(10)
		checkServerAvail()
	else:
		return "Host has been added to the cluster"

def setIpAddresses():
	iscsiIp = socket.gethostbyaddr("iscsi-host" + hostNum + ".jc.rl.ac.uk")[2]
	vxlanIp = socket.gethostbyaddr("host" + hostNum + ".jc.rl.ac.uk")[2]
	return iscsiIp, vxlanIp

def setStaticAddresses():
	(""" This code sets static ip addresses for both the DATA and VXLAN vmkernel ports
""")
	iscsiIp = str(setIpAddresses()[0][0])
	vxlanIp = str(setIpAddresses()[1][0])
	plat.ExecCommand(hostNum, "network ip interface ipv4 set -i vmk1 -I " + iscsiIp + " --netmask 255.255.255.192 --type static")
	plat.ExecCommand(hostNum, "network ip interface ipv4 set -i vmk2 -I " + vxlanIp + " --netmask 255.255.255.192 --type static")

def updateNetapp():
	storageConn = plat.GetStorage()
	netapp = storageConn.netapp
	nettappusername = storageConn.netappusername
	nettapppassword = storageConn.netapppassword
	iqn = getIqn()
	result = subprocess.Popen([
        'sshpass', "-p", nettapppassword, "ssh", nettappusername + "@" + netapp,
	"igroup", "add", "-vserver", "iscsina", "-igroup", "VJASMIN_ESX", "-initiator",  iqn],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	streamdata = result.communicate()
	rc = result.returncode
	stdout = streamdata
	if rc == 0:
		for line in stdout:
			print(line, rc)
			return(line, rc)
			exit(0)
	if rc >= 1:
		for line in stdout:
			print(line, rc)
			return(line, rc)
			exit(1)

def addRoutes():
        # Check if the host is ready
        maintain_routes.fix_routes(hostNum)

def buildEsxHost(server, key):
	("""testDhcp(server, key)
	backupDhcp(server, key)
	copyDhcpConfig(server, key)
	commentInHost()
	commentInBootImage()
	uploadDhcpConfig(server, key)
	testDhcp(server, key)
	restartDhcp(server, key)
	setPXE()
	RebootHost()
	print( "Waiting for host to boot...")
	time.sleep(120)
	commentOutBootImage()
	uploadDhcpConfig(server, key)
	testDhcp(server, key)
	restartDhcp(server, key)
	print("Waiting for host to join cluster. This takes around 10 minutes...")
	checkServerAvail()
	print("Waiting for host to exit maintenance mode...")
	checkMaint()
	setStaticAddresses()
	addRoutes()
	updateNetapp()""")
	enterMaint()
	checkMaint()
	esxReboot()
	checkServerAvail()
	exitMaint()

def decomissionEsxHost(server, key):
        testDhcp(server, key)
        backupDhcp(server, key)
        commentOutHost()
        testDhcp(server, key)
        restartDhcp(server, key)
        RebootHost()
        exit(0)

def main():
	server = "vjasmin-dhcp01.jc.rl.ac.uk"
	key = "/home/cl/id_rsa.key"
	CheckSyntax()
	if identity == "build":
		buildEsxHost(server, key)
	if identity == "decom":
		decomissionEsxHost()
	if identity == "debug":
		checkMaint()

main()
