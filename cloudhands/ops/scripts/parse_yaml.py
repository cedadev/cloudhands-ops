#!/usr/bin/env python
# encoding: UTF-8

import yaml
import pprint
import re
import subprocess

import pkg_resources

Count=0

class Cluster(object):
    def __init__(self, Name, StorageGW, VxlanGW, HostRange):
        self.Name = Name
        # TODO: self.storageGW = storageGW
        self.StorageGW = StorageGW
        self.VxlanGW = VxlanGW
        self.HostRange = HostRange

class IpmiParams(object):
    def __init__(self, Name, Domain, Username, Password):
        self.Name = Name
        self.Domain = Domain
        self.Username = Username
        self.Password = Password

class StorageParams(object):
    def __init__(self, netapp, netappusername, netapppassword):
        self.netapp = netapp
        self.netappusername = netappusername
        self.netapppassword = netapppassword

class LdapParams(object):
    def __init__(self, HostName, Username, Password):
        self.HostName = HostName
        self.Username = Username
        self.Password = Password

class Vcloudparams(object):
    def __init__(self, url, username, password, version, NERCvSEGW, NERCvSENet, Net129GW, Net129Net, Net130GW, Net130Net, Dns1, Dns2, Suffix):
        self.url = url
        self.username = username
        self.password = password
        self.version = version
        self.NERCvSEGW = NERCvSEGW
        self.NERCvSENet = NERCvSENet
        self.Net129GW = Net129GW
        self.Net129Net = Net129Net
        self.Net130GW = Net130GW
        self.Net130Net = Net130Net
        self.Dns1 = Dns1
        self.Dns2 = Dns2
        self.Suffix = Suffix

class Host(object):
    def __init__(self, Number, FullName, ClusterName, StorageGW, VxlanGW, HostRange, StorageNet, VxlanNet):
        self.Number = Number
        self.FullName = FullName
        self.ClusterName = ClusterName
        self.StorageGW = StorageGW
        self.VxlanGW = VxlanGW
        self.HostRange = HostRange
        self.StorageNet = StorageNet
        self.VxlanNet = VxlanNet

class VcenterParams(object):
    def __init__(self, Hostname, Username, Password):
        self.Hostname = Hostname
        self.Username = Username
        self.Password = Password

def evaluateData( config, resource, value ):
    PlatformEnv = config
    if resource == "host":
        host=[]
        domain = PlatformEnv["configuration"]["esxi"]["domain"]
        name = PlatformEnv["configuration"]["esxi"]["name"]
        storageNet = PlatformEnv["configuration"]["esxi"]["storageNet"]
        vxlanNet = PlatformEnv["configuration"]["esxi"]["vxlanNet"]
        Cls=PlatformEnv["clusters"]
        for cl in Cls:
            if Cls[cl]["hostrange"]:
                for HostRange in Cls[cl]["hostrange"]:
                    numbers = re.match("(.*)-(.*)", HostRange)
                    num1 = int(numbers.group(1),base=10)
                    num2 = int(numbers.group(2),base=10)
                    r = range(num1,num2+1)
                    if int(value) in r:
                        host = Host(Number=value, FullName=name + value + domain, ClusterName=cl, StorageGW=Cls[cl]["storageGW"], VxlanGW=Cls[cl]["vxlanGW"], HostRange=Cls[cl]["hostrange"], StorageNet=storageNet, VxlanNet=vxlanNet)
        if not host:
            print("The host number " + value + " is not in a range assigned to any cluster.")
            exit(1)
        return host
    if resource == "cluster":
        Cls=PlatformEnv["clusters"][value]
        cluster = Cluster(Name=value, StorageGW=Cls["storageGW"], VxlanGW=Cls["vxlanGW"], HostRange=Cls["hostrange"])
        return cluster
    if resource == "vcenter":
        VcParams=PlatformEnv["connectionstrings"]["vcenter"]
        vcenterparams = VcenterParams(Hostname=VcParams["hostname"], Username=VcParams["username"], Password=VcParams["password"])
        return vcenterparams
    if resource == "ipmi":
        Ipmiparams = PlatformEnv["connectionstrings"]["ipmi"]
        ipmiparams = IpmiParams(Name=Ipmiparams["name"], Domain=Ipmiparams["domain"], Username=Ipmiparams["username"], Password=Ipmiparams["password"])
        return ipmiparams
    if resource == "ldap":
        Ldapparams = PlatformEnv["connectionstrings"]["ldap"]
        ldapparams = LdapParams(HostName=Ldapparams["hostname"], Username=Ldapparams["username"], Password=Ldapparams["password"])
        return ldapparams
    if resource == "storage":
        Storageparams = PlatformEnv["connectionstrings"]["storage"]
        storageparams = StorageParams(netapp=Storageparams["netapp"], netappusername=Storageparams["netappusername"], netapppassword=Storageparams["netapppassword"])
        return storageparams
    if resource == "vcloud":
        Vcloudyaml=PlatformEnv["connectionstrings"]["vcloud"]
        vcloudparams = Vcloudparams(url=Vcloudyaml["url"], username=Vcloudyaml["username"], password=Vcloudyaml["password"], version=Vcloudyaml["version"], NERCvSEGW=Vcloudyaml["extNets"]["NERCvSEGW"], NERCvSENet=Vcloudyaml["extNets"]["NERCvSENet"], Net129GW=Vcloudyaml["extNets"]["Net129GW"], Net129Net=Vcloudyaml["extNets"]["Net129Net"], Net130GW=Vcloudyaml["extNets"]["Net130GW"], Net130Net=Vcloudyaml["extNets"]["Net130Net"], Dns1=Vcloudyaml["extNets"]["Dns1"], Dns2=Vcloudyaml["extNets"]["Dns2"], Suffix=Vcloudyaml["extNets"]["Suffix"])
        return vcloudparams

def get_config():
    return pkg_resources.resource_string(
        "cloudhands.jasmin", "platform.yml").decode("utf-8")

def GetVcenter():
    return evaluateData(yaml.safe_load(get_config()), "vcenter", "prod")
    
def GetIpmi():
    return evaluateData(yaml.safe_load(get_config()), "ipmi", "prod")

def GetStorage():
    return evaluateData(yaml.safe_load(get_config()), "storage", "prod")

def GetLdap():
    return evaluateData(yaml.safe_load(get_config()), "ldap", "prod")

def GetVcloud():
    return evaluateData(yaml.safe_load(get_config()), "vcloud", "prod")

def GetCluster( ClusterName ):
    return evaluateData(yaml.safe_load(get_config()), "cluster", ClusterName)

#HostNumber must be quoted
def GetHost( HostNumber ):
    return evaluateData(yaml.safe_load(get_config()), "host", HostNumber)

def ExecSshCommand(server, key, command):
    result = subprocess.Popen([
        'ssh', "-i", key, server] + command.split(" "),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    streamdata = result.communicate()
    rc = result.returncode
    stdout = streamdata
    if rc == 0:
        for line in stdout:
            return(line, rc)
            exit(0)
    if rc >= 1:
        for line in stdout:
            return(line, rc)
            exit(1)

def ExecCommand(host, command):
    vcenter = GetVcenter()
    hostObj = GetHost(host).FullName
    result = subprocess.Popen([
        'esxcli', '--server', vcenter.Hostname,
        '--username', vcenter.Username,
        '-h', 'vjasmin-vesx' + str(host) + '.jc.rl.ac.uk',
        '--password', vcenter.Password] + command.split(" "),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    streamdata = result.communicate()
    rc = result.returncode
    stdout = streamdata
    if rc == 0:
        for line in stdout:
            return(line)
            exit(0)
    if rc >= 1:
        print(stdout)
        for line in stdout:
            return(line)
            exit(1)
