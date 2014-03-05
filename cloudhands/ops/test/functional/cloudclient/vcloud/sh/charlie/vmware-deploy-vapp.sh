#!/bin/bash

Authurl='https://*******.rl.ac.uk/'
username='*******@Test_Org'
password='*******'

curl -i -k -H "Accept:application/*+xml;version=5.5" -u $username:$password -X POST ${Authurl}api/sessions > sessionID.txt
xAuth=`grep x-vcloud-authorization sessionID.txt | awk '{print $2}'`

# Get org ref
curl -i -k -H "Accept:application/*+xml;version=5.5" -H "x-vcloud-authorization: ${xAuth}" -X GET ${Authurl}api/org > Ref.txt
OrgRef=`grep href Ref.txt | awk '{print $NF}' | sed 's/href="//g' | sed 's/"\/>//g'`

#Get catalog and vdc ref
curl -i -k -H "Accept:application/*+xml;version=5.5" -H "x-vcloud-authorization: ${xAuth}" -X GET $OrgRef > Ref.txt
CatalogRef=`grep CEMStest Ref.txt | awk '{print $NF}' | sed 's/href="//g' | sed 's/"\/>//g'`
vdcRef=`grep 'TEST ORG' Ref.txt | awk '{print $NF}' | sed 's/href="//g' | sed 's/"\/>//g'`
Network=`grep 'TEST-ORG-EXT-D' Ref.txt | awk '{print $NF}' | sed 's/href="//g' | sed 's/"\/>//g'`

#Get catalog item ref
curl -i -k -H "Accept:application/*+xml;version=5.5" -H "x-vcloud-authorization: ${xAuth}" -X GET $CatalogRef > Ref.txt
TemplateRef=`grep centos6.4-stemcell Ref.txt | awk '{print $NF}' | sed 's/href="//g' | sed 's/"\/>//g'`

#Get vApp Template ref
curl -i -k -H "Accept:application/*+xml;version=5.5" -H "x-vcloud-authorization: ${xAuth}" -X GET $TemplateRef > Ref.txt
Template=`grep centos6.4-stemcell Ref.txt | awk '{print $NF}' | sed 's/href="//g' | sed 's/"\/>//g' | tail -1`

# Create vApp template config
xml='<InstantiateVAppTemplateParams
   xmlns="http://www.vmware.com/vcloud/v1.5"
   xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1"
   name="AppServer-TESTING"
   deploy="false"
   powerOn="false">
   <Description>Testing AppServer</Description>
   <Source
      href="'$Template'" />
</InstantiateVAppTemplateParams>'

# Deploy template and get ref
curl -i -k -H "Accept:application/*+xml;version=5.5" -H "x-vcloud-authorization: ${xAuth}1" -H "Content-Type:application/vnd.vmware.vcloud.instantiateVAppTemplateParams+xml" -X POST ${vdcRef}/action/instantiateVAppTemplate -d "$xml"