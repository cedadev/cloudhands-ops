#!/usr/bin/env python
# encoding: UTF-8
import re
import sys
import parse_yaml as plat

host=plat.GetHost(sys.argv[1])

def checkStorageRoute(host):
	tcpConn = plat.ExecCommand(host.Number, "network ip connection list")
        subnet = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3})\..*", host.StorageGW)
        iscsiConn = re.findall(r"tcp.*:3260.*",tcpConn)
       	for conn in iscsiConn:
		if not re.match(r".*" + str(subnet[0])  + ".*", conn):
			print( "The tcp storage connection on host: " + host.FullName + " looks incorrect\n" + conn )

def checkStoragePaths(host):
	scsiPaths = str(plat.ExecCommand(host.Number, "storage nmp path list"))
	results = re.findall(r"(Runtime Name: .*)\n.*\n.*\n.*(Group State:.*)\n" , scsiPaths, re.MULTILINE)
	arr = [[] for x in xrange(1,12)]
	for result in results:
		if re.match(r".*vmhba37:.*:L1$", result[0]):
			arr[0].append(result)
		if re.match(r".*vmhba37:.*:L2$", result[0]):
                        arr[1].append(result)
                if re.match(r".*vmhba37:.*:L3$", result[0]):
                        arr[2].append(result)
                if re.match(r".*vmhba37:.*:L4$", result[0]):
                        arr[3].append(result)
                if re.match(r".*vmhba37:.*:L5$", result[0]):
                        arr[4].append(result)
                if re.match(r".*vmhba37:.*:L6$", result[0]):
                        arr[5].append(result)
                if re.match(r".*vmhba37:.*:L7$", result[0]):
                        arr[6].append(result)
                if re.match(r".*vmhba37:.*:L8$", result[0]):
                        arr[7].append(result)
                if re.match(r".*vmhba37:.*:L9$", result[0]):
                        arr[8].append(result)
                if re.match(r".*vmhba37:.*:L10$", result[0]):
                        arr[9].append(result)
                if re.match(r".*vmhba37:.*:L11$", result[0]):
                        arr[10].append(result)
                if re.match(r".*vmhba37:.*:L12$", result[0]):
                        arr[11].append(result)
	count1 = 0
	for num in xrange(1,10):
		if len(arr[num]) != 12:
			print "The number of paths available on host: " + host.FullName + " is less than 12. This is incorrect and should be resolved."
		for a in arr[num]:
			if re.match(r"Group State: active$", a[1]):
				count1 = count1 + 1
		if count1 < 3:	
			print "The number of ACTIVE paths available on host: " + host.FullName + " is less than 3. This is incorrect and should be resolved."

checkStorageRoute(host)
checkStoragePaths(host)
