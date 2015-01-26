#!/bin/sh

cmdname=$(basename $0)
cmdline_opt=`getopt hU:i:d:c $*`

usage="Usage: $cmdname [-U vcloud hostname][-i id handle] ...\n
\n
   Options\n
       -h\t\t\tDisplays usage\n
       -U <hostname>\t\tvcloud hostname\n
       -i <id handle>\t\tidentifier handle for this session obtained from login call\n
       -d <identifier>\t\tvDC identifier\n
       -c <directory path>\tDirectory containing the trusted CA (Certificate Authority) certificates.  These are used to\n
       \t\t\tverify the identity of the vCloud Web Service.  Defaults to\n 
       \t\t\tinsecure mode!!\n
"

if [ $? != 0 ] ; then
    echo -e $usage >&2 ;
    exit 1 ;
fi

set -- $cmdline_opt
cadir=

while true ; do
    case "$1" in
        -h) echo -e $usage ; exit 0 ;;
        -U) hostname=$2 ; shift 2 ;;
        -i) id_handle=$2 ; shift 2 ;;
        -d) vdc_id=$2 ; shift 2 ;;
        -c) cadir=$2 ; shift 2 ;;
        --) shift ; break ;;
        *) echo "Error parsing command line" ; exit 1 ;;
    esac
done

if [ "$cadir" ]; then
    ca_setting=" --capath $cadir"
else
    ca_setting=" --insecure"
fi

Authurl="https://$hostname/"

if [ -z vdc_id ]; then
    vdc_id='TEST ORG'
fi

echo Getting Org...
# Get org ref
curl -i -k -H "Accept:application/*+xml;version=5.1" -H "x-vcloud-authorization: ${xAuth}" -X GET ${Authurl}api/org &>Ref.txt
OrgRef=`grep href Ref.txt | awk '{print $NF}' | sed 's/href="//g' | sed 's/"\/>//g'`

echo Getting Org Network...
# Get VDC Ref
curl -i -k -H "Accept:application/*+xml;version=5.1" -H "x-vcloud-authorization: ${xAuth}" -X GET $OrgRef &>Ref.txt
vdcRef=`grep $vdc_id Ref.txt | awk '{print $NF}' | sed 's/href="//g' | sed 's/"\/>//g'`

# Get admin gateway ref
curl -i -k -H "Accept:application/*+xml;version=5.1" -H "x-vcloud-authorization: ${xAuth}" -X GET ${vdcRef} &>Ref.txt
Network=`grep 'edgeGateway' Ref.txt | awk '{print $NF}' | sed 's/href="//g' | sed 's/"\/>//g'`

# Get admin version of gateway
curl -i -k -H "Accept:application/*+xml;version=5.1" -H "x-vcloud-authorization: ${xAuth}" -H "Content-Type:application/vnd.vmware.vcloud.query.records+xml" -X GET ${Network} &>Ref.txt
Gateway=`grep 'EdgeGatewayRecord' Ref.txt | awk '{print $9}' | sed 's/href="//g' | sed 's/"//g'`

# Query Gateway for xml
curl -i -k -H "Accept:application/*+xml;version=5.1" -H "x-vcloud-authorization: ${xAuth}" -H "Content-Type:application/vnd.vmware.vcloud.query.records+xml" -X GET ${Gateway} &>/dev/null > Gateway.xml
EditGateway=`grep 'configureServices' Gateway.xml | awk '{print $NF}' | sed 's/href="//g' | sed 's/"\/>//g'`

# Create XML version of rulebase
echo -e "<EdgeGatewayServiceConfiguration xmlns=\"http://www.vmware.com/vcloud/v1.5\">\n<FirewallService>" > FW.txt
while read line
do
echo test
        name=`echo $line | awk -F, '{print $1}'`
        policy=`echo $line | awk -F, '{print $2}'`
        protocol=`echo $line | awk -F, '{print $3}'`
        if [ "$protocol" == "icmp" ] ; then
                IcmpSubType='<IcmpSubType>any</IcmpSubType>'
        fi
        if [ "$protocol" == "tcp" ]; then
                protocol='<Tcp>true</Tcp>'
        elif [ "$protocol" == "udp" ]; then
                protocol='<Udp>true</Udp>'
        elif [ "$protocol" == "icmp" ]; then
                protocol='<Icmp>true</Icmp>'
        elif [ "$protocol" == "both" ]; then
                protocol='<Tcp>true</Tcp>\n<Udp>true</Udp>'
        fi
        srcPortRange=`echo $line | awk -F, '{print $4}'`
        srcPort=`echo $line | awk -F, '{print $4}'`
        if [ "$srcPortRange" == "any" ] || [ "*-*" ]; then
                srcPort="-1"
        fi
        dstPortRange=`echo $line | awk -F, '{print $5}'`
        dstPort=`echo $line | awk -F, '{print $5}'`
        if [ "$dstPortRange" == "any" ] || [ "*-*" ]; then
                dstPort="-1"
        fi
        src=`echo $line | awk -F, '{print $6}'`
        dst=`echo $line | awk -F, '{print $7}'`
echo -e "
                <FirewallRule>
                    <IsEnabled>true</IsEnabled>
                    <MatchOnTranslate>false</MatchOnTranslate>
                    <Description>$name</Description>
                    <Policy>$policy</Policy>
                    <Protocols>
                        $protocol
                    </Protocols>
                    $IcmpSubType
                    <Port>$dstPort</Port>
                    <DestinationPortRange>$dstPortRange</DestinationPortRange>
                    <DestinationIp>$dst</DestinationIp>
                    <SourcePort>$srcPort</SourcePort>
                    <SourcePortRange>$srcPortRange</SourcePortRange>
                    <SourceIp>$src</SourceIp>
                    <EnableLogging>true</EnableLogging>
                </FirewallRule>" >> FW.txt
done < rules.txt
echo -e "</FirewallService>\n</EdgeGatewayServiceConfiguration>" >> FW.txt

###############################################
# Update Gateway
curl -i -k  -H "Accept:application/*+xml;version=5.5" -H "x-vcloud-authorization: ${xAuth}x" -H "Content-Type:application/vnd.vmware.admin.edgeGatewayServiceConfiguration+xml" -X POST ${EditGateway} -d @FW.txt

# Logout
curl -i -k -H "Accept:application/*+xml;version=5.5" -H "x-vcloud-authorization: ${xAuth}" -X DELETE ${Authurl}api/sessions
exit
