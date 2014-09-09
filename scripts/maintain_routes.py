#!/usr/bin/env python
# encoding: UTF-8
__author__ = 'cl'

import parse_yaml as plat
import re
import subprocess
import sys

host = plat.GetHost(sys.argv[2])
vcenter = plat.GetVcenter()
cmd = "esxcli --server " + vcenter.Hostname + " --username \"" + vcenter.Username + "\" --password \"" + vcenter.Password + "\" -h "

def check_route():
    output = 0
    routes = plat.ExecCommand(host.Number, "network ip route ipv4 list")
    (""" remove the cidr suffix so we get just the network address """)
    storageNet = re.match(r"(.*)/.*", host.StorageNet).group(1)
    vxlanNet = re.match(r"(.*)/.*", host.VxlanNet).group(1)
    #query host to return storage routing information
    res = re.findall(r".*" + storageNet + ".*" + host.StorageGW + ".*vmk1.*", str(routes), re.MULTILINE)
    if not res:
        print("storage route is missing from host" + host.FullName)
        output = output + 1
    else:
        print("storage routes are already added to " + host.FullName)
    #query host to return VXLAN routing information
    routes = data = plat.ExecCommand(host.Number, "network ip route ipv4 list --netstack=vxlan")
    res = re.findall(r".*" + vxlanNet + ".*" + host.VxlanGW + ".*vmk2.*", str(routes), re.MULTILINE)
    if not res:
        print("VXLAN route is missing from host" + host.FullName)
        output = output + 2
    else:
        print("VXLAN routes are already added to " + host.FullName)
    return output

def set_route(type):
    if type == "storage":
        plat.ExecCommand(host.Number, "network ip route ipv4 add --gateway " + host.StorageGW + " --network " + host.StorageNet)
    if type == "vxlan":
        plat.ExecCommand(host.Number, "network ip route ipv4 add --gateway " + host.VxlanGW + " --network " + host.VxlanNet + " --netstack=vxlan")

def fix_routes(host):
    res = check_route()
    if res == 0:
        print("no routes on host " + host + " need fixing" )
    if res == 1:
        print("Adding storage routes to " + host)
        set_route("storage")
    if res == 2:
        print("Adding VXLAN routes to " + host)
        set_route("vxlan")
    if res == 3:
        print("Adding Storage and VXLAN routes to " + host)
        set_route("storage")
        set_route("vxlan")

def run():
    if sys.argv[1] == "check":
        check_route()
    if sys.argv[1] == "fix":
        fix_routes(host.Number)

def main():
    if int(len(sys.argv)) <= 2:
        print(sys.argv[0] + " <check|fix> <host number>")
        exit(1)
    run()

main()
