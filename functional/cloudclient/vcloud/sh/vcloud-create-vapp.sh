#!/bin/sh
cmdname=$(basename $0)
cmdline_opt=`getopt hU:i:a:d:n:c $*`

usage="Usage: $cmdname [-U vcloud hostname][-i id handle] ...\n
\n
   Options\n
       -h\t\t\tDisplays usage\n
       -U <hostname>\t\tvcloud hostname\n
       -i <id handle>\t\tidentifier handle for this session obtained from login call\n
       -d <identifier>\t\tvDC identifier\n
       -a <identifier>\t\tvApp template identifier\n
       -n <vapp name>\t\tname of vApp to be created\n
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
        -a) vapp_id=$2 ; shift 2 ;;
        -d) vdc_id=$2 ; shift 2 ;;
        -n) vapp_name=$2 ; shift 2 ;;
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

#req="<InstantiateVAppTemplateParams deploy=\"false\" name=\"$vapp_name\" powerOn=\"false\" xml:lang=\"en\" xmlns=\"http://www.vmware.com/vcloud/v1.5\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"><Source href=\"https://$hostname/api/vAppTemplate/$vapp_id\" /></InstantiateVAppTemplateParams>"

read -d '' req <<- EOF
<InstantiateVAppTemplateParams
    deploy="false"
    name="$vapp_name"
    powerOn="false"
    xml:lang="en"
    xmlns="http://www.vmware.com/vcloud/v1.5"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <Source href="https://$hostname/api/vAppTemplate/$vapp_id" />
</InstantiateVAppTemplateParams>"
EOF
 
curl -X POST \
	"https://cm005.cems.rl.ac.uk/api/vdc/$vdc_id/action/instantiateVAppTemplate" \
	-H 'Content-Type: application/vnd.vmware.vcloud.instantiateVAppTemplateParams+xml' \
	-H "Content-length: ${#req}" \
	-H "x-vcloud-authorization: $id_handle" \
	-H 'Accept: application/*+xml;version=1.5' \
	-H 'User-Agent: libcloud/0.13.2 (vCloud)' \
	-H "Host: $hostname" \
	--data "$req" \
	$ca_setting
