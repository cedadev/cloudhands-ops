#!/usr/bin/env python
# encoding: UTF-8

__author__ = 'cl'

import parse_yaml as plat
import csv
from vCloudHTTP import vCloudHTTP
from vCloudXMLReader import vCloudXMLReader
import re
import time
import sys
import os.path
from ldap3 import Server, Connection, STRATEGY_SYNC, AUTH_SIMPLE
from ldap3 import SEARCH_SCOPE_WHOLE_SUBTREE, SEARCH_DEREFERENCE_ALWAYS, STRATEGY_LDIF_PRODUCER

class setupOrg(object):

    def connectionStr(self):
        # This method builds a connection string for vCloud from details defined in the platform.yml
        return plat.GetVcloud()

    def auth(self):
        # This method requests a token for authenitcation
        return vCloudHTTP.login(self.connectionStr().url, self.connectionStr().username, self.connectionStr().password, self.connectionStr().version)

    def createorg(self, orgName, orgFullName, orgDesc, auth):
        # This method creates the organisation within vCloud
        xml = ("""<?xml version="1.0" encoding="UTF-8"?>
    <AdminOrg
       xmlns="http://www.vmware.com/vcloud/v1.5"
       name="ORGNAME"
       type="application/vnd.vmware.admin.organization+xml">
       <Description>ORGDESC</Description>
       <FullName>ORGFULLNAME</FullName>
       <IsEnabled>true</IsEnabled>
       <Settings>
          <OrgGeneralSettings>
             <CanPublishCatalogs>false</CanPublishCatalogs>
             <DeployedVMQuota>0</DeployedVMQuota>
             <StoredVmQuota>0</StoredVmQuota>
             <UseServerBootSequence>false</UseServerBootSequence>
             <DelayAfterPowerOnSeconds>0</DelayAfterPowerOnSeconds>
          </OrgGeneralSettings>
          <VAppLeaseSettings>
            <DeploymentLeaseSeconds>0</DeploymentLeaseSeconds>
            <StorageLeaseSeconds>0</StorageLeaseSeconds>
          </VAppLeaseSettings>
          <VAppTemplateLeaseSettings>
            <StorageLeaseSeconds>0</StorageLeaseSeconds>
          </VAppTemplateLeaseSettings>
          <OrgLdapSettings>
             <OrgLdapMode>SYSTEM</OrgLdapMode>
             <CustomUsersOu />
          </OrgLdapSettings>
          <OrgEmailSettings>
             <IsDefaultSmtpServer>true</IsDefaultSmtpServer>
             <IsDefaultOrgEmail>true</IsDefaultOrgEmail>
             <FromEmailAddress />
             <DefaultSubjectPrefix />
             <IsAlertEmailToAllAdmins>true</IsAlertEmailToAllAdmins>
            </OrgEmailSettings>
       </Settings>
    </AdminOrg>""")
        xml = re.sub(r"ORGNAME", orgName, xml)
        xml = re.sub(r"ORGFULLNAME", orgFullName, xml)
        xml = re.sub(r"ORGDESC", orgDesc, xml)
        #Setting up vCloud director organisation
        print("Setting up vCloud director organisation...")
        xmlreturn = vCloudHTTP.httpPOST(self.connectionStr().url + "/api/admin/orgs", "application/vnd.vmware.admin.organization+xml", auth, xml, self.connectionStr().version)
        response = vCloudXMLReader()
        response.parseString(xmlreturn)
        return response.getAttrValue(".", "href")

    def getProviderVdc(self, auth, name):
        # This function returns the correct provider VDC to use based on the parameters passed in from the work request
        xmlreturn = vCloudHTTP.httpGET(self.connectionStr().url + "/api/admin", auth, self.connectionStr().version)
        response = vCloudXMLReader()
        response.parseString(xmlreturn)
        ###### EXAMPLE ######
        ##for i in response.getElementsList("vcloud:ProviderVdcReferences/vcloud:ProviderVdcReference"):
        ##   print(i.attrib.get("name"))
        ##for p in response.getAttrValueList("vcloud:ProviderVdcReferences/vcloud:ProviderVdcReference", "name"):
        ##    print(p)
        for pvdc in response.getElementsList("vcloud:ProviderVdcReferences/vcloud:ProviderVdcReference"):
            if pvdc.attrib.get("name") == name:
               return pvdc.attrib.get("href")

    def getProviderVdcNetworks(self, auth, url):
        xmlreturn = vCloudHTTP.httpGET(url, auth, self.connectionStr().version)
        response = vCloudXMLReader()
        response.parseString(xmlreturn)
        arr = list()
        for pvdc in response.getElementsList("vcloud:AvailableNetworks/vcloud:Network"):
            val={pvdc.get("name"):pvdc.get("href")}
            arr.append(val)
        return arr

    def createVdc(self, newOrgRef, vdcName, pvdcHref, memAlloc, cpuAlloc, storageAlloc, netPool, storageProfile, auth):
        xml = ("""<?xml version="1.0" encoding="UTF-8"?>
    <CreateVdcParams
       name="VDCNAME"
       xmlns="http://www.vmware.com/vcloud/v1.5">
       <Description>VDCDESC</Description>
       <AllocationModel>AllocationVApp</AllocationModel>
       <ComputeCapacity>
          <Cpu>
             <Units>MHz</Units>
             <Allocated>CPUALLOC</Allocated>
             <Limit>CPUALLOC</Limit>
          </Cpu>
          <Memory>
             <Units>MB</Units>
             <Allocated>MEMALLOC</Allocated>
             <Limit>MEMALLOC</Limit>
          </Memory>
       </ComputeCapacity>
       <NicQuota>0</NicQuota>
       <NetworkQuota>100</NetworkQuota>
       <VdcStorageProfile>
       <Enabled>true</Enabled>
          <Units>MB</Units>
          <Limit>STORAGEALLOC</Limit>
          <Default>true</Default>
          <ProviderVdcStorageProfile
             href="STORAGEPROFILE" />
       </VdcStorageProfile>
       <ResourceGuaranteedMemory>1</ResourceGuaranteedMemory>
       <ResourceGuaranteedCpu>0.2</ResourceGuaranteedCpu>
       <VCpuInMhz>2600</VCpuInMhz>
       <IsThinProvision>false</IsThinProvision>
       <NetworkPoolReference
          href="NETPOOL"/>
       <ProviderVdcReference
          name="Main Provider"
          href="PVDCHREF" />
       <UsesFastProvisioning>false</UsesFastProvisioning>
    </CreateVdcParams>""")
        xml = re.sub(r"VDCNAME", vdcName, xml)
        xml = re.sub(r"VDCDESC", vdcName, xml)
        xml = re.sub(r"PVDCHREF", pvdcHref, xml)
        xml = re.sub(r"CPUALLOC", cpuAlloc, xml)
        xml = re.sub(r"MEMALLOC", memAlloc, xml)
        xml = re.sub(r"NETPOOL", netPool, xml)
        xml = re.sub(r"STORAGEPROFILE", storageProfile, xml)
        xml = re.sub(r"STORAGEALLOC", storageAlloc, xml)
        print("Setting up vCloud director virtual datacentre...")
        xmlreturn = vCloudHTTP.httpPOST(newOrgRef + "/vdcsparams", "application/vnd.vmware.admin.createVdcParams+xml", auth, xml, self.connectionStr().version)
        response = vCloudXMLReader()
        response.parseString(xmlreturn)
        return response.getAttrValue(".", "href")

    def createEdgeGateway(self, edgeName, extNetHref, edgeIp, endRange, gateway, netmask, newVdcRef, auth):
        xml = ("""<?xml version="1.0" encoding="UTF-8"?>
<EdgeGateway xmlns="http://www.vmware.com/vcloud/v1.5" name="EDGENAME">
    <Description>"External internet access"</Description>
    <Configuration>
        <GatewayBackingConfig>full4</GatewayBackingConfig>
        <GatewayInterfaces>
            <GatewayInterface>
                <Name>NERCvSE - UN-managed-cloud-external-internet</Name>
                <DisplayName>NERCvSE - UN-managed-cloud-external-internet</DisplayName>
                <Network href="EXTNETHREF" />
                <InterfaceType>uplink</InterfaceType>
                <SubnetParticipation>
                    <Gateway>GATEWAY</Gateway>
                    <Netmask>NETMASK</Netmask>
                    <IpAddress>EDGEIP</IpAddress>
                    <IpRanges>
                        <IpRange>
                            <StartAddress>EDGEIP</StartAddress>
                            <EndAddress>ENDRANGE</EndAddress>
                        </IpRange>
                    </IpRanges>
                </SubnetParticipation>
                <ApplyRateLimit>false</ApplyRateLimit>
                <InRateLimit>100.0</InRateLimit>
                <OutRateLimit>100.0</OutRateLimit>
                <UseForDefaultRoute>true</UseForDefaultRoute>
            </GatewayInterface>
        </GatewayInterfaces>
        <EdgeGatewayServiceConfiguration>
            <FirewallService>
                <IsEnabled>true</IsEnabled>
                <DefaultAction>drop</DefaultAction>
                <LogDefaultAction>false</LogDefaultAction>
                <FirewallRule>
                    <Id>1</Id>
                    <IsEnabled>true</IsEnabled>
                    <MatchOnTranslate>false</MatchOnTranslate>
                    <Description>OUTBOUND-HTTP</Description>
                    <Policy>allow</Policy>
                    <Protocols>
                        <Tcp>true</Tcp>
                    </Protocols>
                    <Port>80</Port>
                    <DestinationPortRange>80</DestinationPortRange>
                    <DestinationIp>Any</DestinationIp>
                    <SourcePort>-1</SourcePort>
                    <SourcePortRange>Any</SourcePortRange>
                    <SourceIp>internal</SourceIp>
                    <EnableLogging>true</EnableLogging>
                </FirewallRule>
                <FirewallRule>
                    <Id>2</Id>
                    <IsEnabled>true</IsEnabled>
                    <MatchOnTranslate>false</MatchOnTranslate>
                    <Description>OUTBOUND-HTTPS</Description>
                    <Policy>allow</Policy>
                    <Protocols>
                        <Tcp>true</Tcp>
                    </Protocols>
                    <Port>443</Port>
                    <DestinationPortRange>443</DestinationPortRange>
                    <DestinationIp>Any</DestinationIp>
                    <SourcePort>-1</SourcePort>
                    <SourcePortRange>Any</SourcePortRange>
                    <SourceIp>internal</SourceIp>
                    <EnableLogging>true</EnableLogging>
                </FirewallRule>
                <FirewallRule>
                    <Id>3</Id>
                    <IsEnabled>true</IsEnabled>
                    <MatchOnTranslate>false</MatchOnTranslate>
                    <Description>OUTBOUND-SSH</Description>
                    <Policy>allow</Policy>
                    <Protocols>
                        <Tcp>true</Tcp>
                    </Protocols>
                    <Port>22</Port>
                    <DestinationPortRange>22</DestinationPortRange>
                    <DestinationIp>Any</DestinationIp>
                    <SourcePort>-1</SourcePort>
                    <SourcePortRange>Any</SourcePortRange>
                    <SourceIp>internal</SourceIp>
                    <EnableLogging>true</EnableLogging>
                </FirewallRule>
                <FirewallRule>
                    <Id>4</Id>
                    <IsEnabled>true</IsEnabled>
                    <MatchOnTranslate>false</MatchOnTranslate>
                    <Description>OUTBOUND-DNS</Description>
                    <Policy>allow</Policy>
                    <Protocols>
                        <Udp>true</Udp>
                    </Protocols>
                    <Port>53</Port>
                    <DestinationPortRange>53</DestinationPortRange>
                    <DestinationIp>Any</DestinationIp>
                    <SourcePort>-1</SourcePort>
                    <SourcePortRange>Any</SourcePortRange>
                    <SourceIp>internal</SourceIp>
                    <EnableLogging>true</EnableLogging>
                </FirewallRule>
                <FirewallRule>
                    <Id>5</Id>
                    <IsEnabled>true</IsEnabled>
                    <MatchOnTranslate>false</MatchOnTranslate>
                    <Description>OUTBOUND-ICMP</Description>
                    <Policy>allow</Policy>
                    <Protocols>
                        <Icmp>true</Icmp>
                    </Protocols>
                    <IcmpSubType>any</IcmpSubType>
                    <Port>-1</Port>
                    <DestinationPortRange>Any</DestinationPortRange>
                    <DestinationIp>Any</DestinationIp>
                    <SourcePort>-1</SourcePort>
                    <SourcePortRange>Any</SourcePortRange>
                    <SourceIp>internal</SourceIp>
                    <EnableLogging>false</EnableLogging>
                </FirewallRule>
            </FirewallService>
            <NatService>
                <IsEnabled>true</IsEnabled>
                <NatRule>
                    <RuleType>SNAT</RuleType>
                    <IsEnabled>true</IsEnabled>
                    <Id>65537</Id>
                    <GatewayNatRule>
                        <Interface type="application/vnd.vmware.admin.network+xml" href="EXTNETHREF"/>
                        <OriginalIp>192.168.3.0/24</OriginalIp>
                        <TranslatedIp>EDGEIP</TranslatedIp>
                    </GatewayNatRule>
                </NatRule>
            </NatService>
        </EdgeGatewayServiceConfiguration>
        <HaEnabled>true</HaEnabled>
        <UseDefaultRouteForDnsRelay>false</UseDefaultRouteForDnsRelay>
    </Configuration>
</EdgeGateway>
        """)
        xml = re.sub(r"EDGENAME", edgeName, xml)
        xml = re.sub(r"EXTNETHREF", extNetHref, xml)
        xml = re.sub(r"EDGEIP", edgeIp, xml)
        xml = re.sub(r"ENDRANGE", endRange, xml)
        xml = re.sub(r"GATEWAY", gateway, xml)
        xml = re.sub(r"NETMASK", netmask, xml)
        print("Setting up vShield Gateway...")
        xmlreturn = vCloudHTTP.httpPOST(newVdcRef + "/edgeGateways", "application/vnd.vmware.admin.edgeGateway+xml", auth, xml, self.connectionStr().version)
        arr = list()
        response = vCloudXMLReader()
        response.parseString(xmlreturn)
        ##response.parseFile("gateway.xml")
        tasks = response.getElementsList("vcloud:Tasks/vcloud:Task")
        href = response.getAttrValue(".", "href")
        for task in tasks:
            arr.append(task.get("href"))
        arr.append(href)
        return arr

    def readWorkRequest(self, filename):
        dataArr = {}
        data = csv.reader(open(filename), delimiter=',')
        for row in data:
            dataArr[row[0]] = row[1]
        return dataArr

    def calcIPRange(self, edgeIp):
        ip = re.match(r"(^\d{1,3}\.\d{1,3}\.\d{1,3}\.)(\d{1,3}$)", edgeIp).group(1,2)
        ipend = int(ip[1]) + 3
        ip = ip[0] + str(ipend)
        return ip

    def checkTask(self, url, auth):
        xmlreturn = vCloudHTTP.httpGET(url, auth, self.connectionStr().version)
        response = vCloudXMLReader()
        response.parseString(xmlreturn)
        status = response.getAttrValue(".", "status")
        task = response.getAttrValue(".", "operationName")
        for error in response.getAttrValueList("vcloud:Error", "stackTrace"):
            error = error
        if status == "error":
            print("The task " + task + " failed with the following error:\n" + error)
            return False
        if status != "success":
            print("waiting for task " + task + "to complete. This can take some time...")
            time.sleep(30)
            self.checkTask(url, auth)

    def createOrgNet(self, edgeName, dns1, dns2, suffix, newEdgeRef, newVdcRef, auth):
        xml = ("""<?xml version="1.0" encoding="UTF-8"?>
<OrgVdcNetwork
   name="EDGENAME"
   xmlns="http://www.vmware.com/vcloud/v1.5">
   <Description>Routed through an Edge Gateway</Description>
   <Configuration>
      <IpScopes>
         <IpScope>
            <IsInherited>false</IsInherited>
            <Gateway>192.168.3.1</Gateway>
            <Netmask>255.255.255.0</Netmask>
            <Dns1>DNS1</Dns1>
            <Dns2>DNS2</Dns2>
            <DnsSuffix>SUFFIX</DnsSuffix>
            <IpRanges>
               <IpRange>
                  <StartAddress>192.168.3.2</StartAddress>
                  <EndAddress>192.168.3.254</EndAddress>
               </IpRange>
            </IpRanges>
         </IpScope>
      </IpScopes>
      <FenceMode>natRouted</FenceMode>
   </Configuration>
   <EdgeGateway
      href="NEWEDGEREF" />
   <IsShared>true</IsShared>
</OrgVdcNetwork>""")
        xml = re.sub(r"NEWEDGEREF", newEdgeRef, xml)
        xml = re.sub(r"EDGENAME", edgeName, xml)
        xml = re.sub(r"DNS1", dns1, xml)
        xml = re.sub(r"DNS2", dns2, xml)
        xml = re.sub(r"SUFFIX", suffix, xml)
        print("Setting up Org Network...")
        xmlreturn = vCloudHTTP.httpPOST(newVdcRef + "/networks", "application/vnd.vmware.vcloud.orgVdcNetwork+xml", auth, xml, self.connectionStr().version)

    def createCatalog(self, OrgName, newOrgRef, auth):
        xml = ("""<?xml version="1.0" encoding="UTF-8"?>
<AdminCatalog xmlns="http://www.vmware.com/vcloud/v1.5" name="ORGNAME">
   <Description>Private Catalog</Description>
</AdminCatalog>""")
        xml = re.sub(r"ORGNAME", OrgName + "-private-catalog", xml)
        print("Setting up private catalog")
        xmlreturn = vCloudHTTP.httpPOST(newOrgRef + "/catalogs", "application/vnd.vmware.admin.catalog+xml", auth, xml, self.connectionStr().version)
        return xmlreturn

    def shareCatalog(self, pubCat, newOrgRef, auth):
        catlogRef = re.sub("/action", "", pubCat)
        xml = vCloudHTTP.httpGET(catlogRef, auth, self.connectionStr().version)
        xml = re.sub(r"<AccessSettings>", "<AccessSettings>\n\t\t<AccessSetting>\n\t\t\t<Subject type=\"application/vnd.vmware.admin.organization+xml\" href=\"" + newOrgRef + "\"/>\n\t\t\t<AccessLevel>ReadOnly</AccessLevel>\n\t\t</AccessSetting>", xml)
        print("Sharing public catalog")
        xmlreturn = vCloudHTTP.httpPOST(pubCat, "application/vnd.vmware.vcloud.controlAccess+xml", auth, xml, self.connectionStr().version)
        return xmlreturn

#    def createJVO(self, orgName, guestCustName):
#        ssh datbaseUser@portalDatabaseHost -C "run script" + orgName + " " + guestCustName

    def updateLdap(self, orgName):
       print("test")

    def updateLdap(self, orgName):
        print("Adding groups to LDAP...")
        ldapconn = plat.GetLdap()
        LDAP_HOST = ldapconn.HostName
        LDAP_USER = ldapconn.Username
        LDAP_PASS = ldapconn.Password
        BASE="ou=jasmin2,ou=Groups,o=hpc,dc=rl,dc=ac,dc=uk"
        server = Server(LDAP_HOST, port = 389)
        connection = Connection(server, auto_bind = False,
            user=LDAP_USER, password=LDAP_PASS, authentication=AUTH_SIMPLE)
        connection.open()
        connection.bind()
        ("""
        #This block can be useful to perform searches against LDAP. It outputs the results as an LDIF.
        #connection.search(search_base = BASE, search_filter = '(objectClass=posixGroup)', search_scope = SEARCH_SCOPE_WHOLE_SUBTREE, attributes = ['cn', 'givenName'])
        #print('Search result:')
        #print(connection.response_to_ldif())
        """)
        # We now return all the gidNumbers under the jasmin2 tree to find the next contiguous free gidNumber
        connection.search(search_base = BASE, search_filter = '(objectClass=posixGroup)', search_scope = SEARCH_SCOPE_WHOLE_SUBTREE, attributes = ['gidNumber'])
        highNum = 201001
        for res in connection.response:
            currentNum = int(res['attributes']['gidNumber'][0])
            if currentNum > highNum:
                highNum = currentNum
        GID = highNum + 1
        connection.add('cn=' + orgName + '-vcloud_admins,' + BASE, 'posixGroup', {'objectClass': 'posixGroup',
                                                                  'gidNumber': GID, 'cn': orgName + '-vcloud_admins'})
        connection.add('cn=' + orgName + '-vcloud_users,' + BASE, 'posixGroup', {'objectClass': 'posixGroup',
                                                                  'gidNumber': GID + 1, 'cn': orgName + '-vcloud_users'})
        connection.add('cn=' + orgName + '-vcloud_console,' + BASE, 'posixGroup', {'objectClass': 'posixGroup',
                                                                  'gidNumber': GID + 2, 'cn': orgName + '-vcloud_console'})

    def redeployVse(self, newEdgeRef):
        vCloudHTTP.httpPOST(newEdgeRef + "/action/redeploy", "application/vnd.vmware.admin.edgeGateway+xml", self.auth(), "", self.connectionStr().version)

def createEntireTennacy(filename):
    # This method is responsible for calling the other methods to actually implement the tenancy.
    # It reads the work requests and sets the relevent variables based on the type of tenancy being requested.
    # If requirements for how the resources are allocated are changed this
    # is the place to update the variables used as teh values set in vCloud director
    org = setupOrg()
    orgParams = org.readWorkRequest(filename)
    if orgParams["resource type"] == "high-compute":
        cpuAlloc=int(orgParams["high-compute vCPU cores requested"]) * 2600
        cpuAlloc=str(cpuAlloc)
        memAlloc=orgParams["high compute RAM requested"] + "000"
        netPool="https://vcloud.ceda.ac.uk/api/admin/extension/networkPool/c433bec2-6dd0-41a2-bcab-8272b69d2c5b"
        storageProfile="https://vcloud.ceda.ac.uk/api/admin/pvdcStorageProfile/0488ffb2-8163-4880-b386-06b808da884d"
    else:
        cpuAlloc=int(orgParams["std-compute vCPU cores requested"]) * 2600
        cpuAlloc=str(cpuAlloc)
        memAlloc=orgParams["std compute RAM requested"] + "000"
        netPool="https://vcloud.ceda.ac.uk/api/admin/extension/networkPool/f2f39380-cd90-4963-8210-d29e98f29900"
        storageProfile="https://vcloud.ceda.ac.uk/api/admin/pvdcStorageProfile/0488ffb2-8163-4880-b386-06b808da884d"
    if orgParams["Managed or un-managed"] == "managed":
        guestCustName = "/root/managed-post-cust.sh"
        orgName = orgParams["organisation name"] + "-M"
        dns1 = org.connectionStr().Dns1
        dns2 = org.connectionStr().Dns2
        suffix = org.connectionStr().Suffix
        pubCat = "https://vcloud.ceda.ac.uk/api/org/f6a5f09b-9981-40e8-9f90-2f03d26fbedf/catalog/20eafefd-9a73-4003-894d-2f12ba9a76a5/action/controlAccess/"
    else:
        orgName = orgParams["organisation name"] + "-U"
        guestCustName = "/root/un-managed-post-cust.sh"
        dns1 = "8.8.8.8"
        dns2 = ""
        suffix = ""
        pubCat = "https://vcloud.ceda.ac.uk/api/org/f6a5f09b-9981-40e8-9f90-2f03d26fbedf/catalog/acc29263-c877-4be6-b070-8ce7b518280e/action/controlAccess/"
    if orgParams["External network"] == "net129":
        extNetHref = "https://vcloud.ceda.ac.uk/api/admin/network/48147f14-651e-4f0f-a98b-aa553786486c"
        gateway = org.connectionStr().Net129GW
        netmask = org.connectionStr().Net129Net
    elif orgParams["External network"] == "net130":
        extNetHref = "https://vcloud.ceda.ac.uk/api/admin/network/70e10960-b286-4430-972a-82c9771a5301"
        gateway = org.connectionStr().Net130GW
        netmask = org.connectionStr().Net130Net
    else:
        extNetHref = "https://vcloud.ceda.ac.uk/api/admin/network/281bb015-4dbe-4df4-9b7f-bd7de9431c3e"
        gateway = org.connectionStr().NERCvSEGW
        netmask = org.connectionStr().NERCvSENet
    vdcName = orgName + "-" + orgParams["resource type"]
    # Convert storage from GB to MB
    storageAlloc = orgParams["Storage requested"] + "000"
    edgeName = orgName + "-" + orgParams["External network"]
    edgeIp = orgParams["vShield edge IP"]
    endRange = org.calcIPRange(edgeIp)
    #("""
    newOrgRef = org.createorg(orgName, orgParams["Organisation Full Name"], orgParams["Description"], org.auth())
    print(newOrgRef)
    pvdcRef = org.getProviderVdc(org.auth(), orgParams["resource type"])
    newVdcRef = org.createVdc(newOrgRef, vdcName, pvdcRef, memAlloc, cpuAlloc, storageAlloc, netPool, storageProfile, org.auth())
    print(newVdcRef)
    newEdgeRef = org.createEdgeGateway(edgeName, extNetHref, edgeIp, endRange, gateway, netmask, newVdcRef, org.auth())
    print(newEdgeRef[1])
    org.checkTask(newEdgeRef[0], org.auth())
    org.createOrgNet(edgeName, dns1, dns2, suffix, newEdgeRef[1], newVdcRef, org.auth())
    org.createCatalog(orgName, newOrgRef, org.auth())
    org.shareCatalog(pubCat, newOrgRef, org.auth())
    org.updateLdap(orgName)
    org.redeployVse(newEdgeRef[1])
    #""")

    #### Testing
    ("""
    org.updateLdap("test")
    #newOrgRef = "https://vcloud.ceda.ac.uk/api/admin/org/87d2ca23-9740-4e23-ad03-55b0318b4b49"
    #newVdcRef = "https://vcloud.ceda.ac.uk/api/admin/vdc/141ba9e8-96a4-4a27-99cd-06673c7e9fe8"
    #newEdgeRef = org.createEdgeGateway(edgeName, extNetHref, edgeIp, endRange, gateway, netmask, newVdcRef, org.auth())
    #newEdgeRef = "https://vcloud.ceda.ac.uk/api/task/4114c54b-f247-49b6-b404-112b3d051fe2"
    #print(org.createCatalog(orgName, newOrgRef, org.auth()))
    #org.createOrgNet(edgeName, dns1, dns2, suffix, newEdgeRef, newVdcRef, org.auth())
    #org.shareCatalog(pubCat, newOrgRef, org.auth())
    #print(vCloudHTTP.httpGET("https://vcloud.ceda.ac.uk/api/admin/org/a7ac6791-04fc-494e-a374-0037a35d322a", org.auth(), org.connectionStr().version))
    """)

file = None
if len(sys.argv) <= 1:
	print(sys.argv[0] + " <full path to file>")
	exit(1)
file = sys.argv[1]
try:
	open(file)
except IOError as e:
	print( "File does not exist. Please input the full file path" )
	exit(1)
		
createEntireTennacy(file)




