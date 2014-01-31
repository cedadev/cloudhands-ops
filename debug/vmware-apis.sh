#! /bin/bash -

# This boilerplate from 'Classic Shell Scripting'

IFS='
    '
OLDPATH="$PATH"
PATH="/bin:/usr/bin"
export PATH

EXITCODE=0
PROGRAM=$( basename "$0" )
DIR=$( cd "$( dirname "$0" )" && pwd )
PARENT=$(readlink -e "$DIR/..")
SETTINGS="phase01"


usage()
{
    echo "Usage: $PROGRAM [--settings SETTINGS]"
}

usage_and_exit()
{
    usage
    exit "$1"
}

info()
{
    echo -e "\e[2m$@\e[0m" 1>&2
}

warning()
{
    echo -e "\e[1m$@\e[0m" 1>&2
    EXITCODE=$(($EXITCODE + 1))
}

error()
{
    warning "$@"
    usage_and_exit 1
}

version()
{
    VERSION=$(head "$PARENT/cloudhands/ops/__init__.py" | cut -d= -f2 | tr -d '" ')
    echo "$PROGRAM $VERSION"
}

# End of boilerplate

read_endpoint()
{
    # Read the variables 'name', 'port' and 'api_version' from the user section
    # of a config file
    if [ -f "$CFG" ]
    then
        while read -r key value; do
            eval "host_$key"="\$value"
        done < <(grep -A3 '\[host\]' $CFG \
                | tr -d ' ' | cut -s -d'=' -f1,2 --output-delimiter=" ")
    else
        warning "Could not find settings ($CFG)"
        exit 0
    fi
}

read_credentials()
{
    # Read the variables 'name' and 'pass' from the user section of a config
    # file
    if [ -f "$CFG" ]
    then
        while read -r key value; do
            eval "user_$key"="\$value"
        done < <(grep -A2 '\[user\]' $CFG \
                | tr -d ' ' | cut -s -d'=' -f1,2 --output-delimiter=" ")
    else
        warning "Could not find settings ($CFG)"
        exit 0
    fi
}

url_get() # token, url
{
    curl -s -i -k -H "Accept:application/*+xml;version="$host_api_version"" \
    -H "$1" -X GET "$2"
}

api_versions()
{
    REPLY=`curl -s -k \
    -H "Accept:application/*+xml;version=1.5" -X GET \
    https://"$host_name":"$host_port"/api/versions`
    echo "$REPLY" | tr ' ' '\n' | grep -E -o "v[[:digit:]]*\.[[:digit:]]*" \
    | sort | uniq | wc -l
}

api_login() # user name, password
{
    curl -s -i -k -u "$1:$2" \
    -H "Accept:application/*+xml;version="$host_api_version"" -X POST  \
    https://"$host_name":"$host_port"/api/sessions \
    | grep 'x-vcloud-authorization.*'
}

api_org_get() # authorization token header
{
    curl -s -i -k -H "Accept:application/*+xml;version="$host_api_version"" \
    -H "$1" -X GET \
    https://"$host_name":"$host_port"/api/org
}

proc_get_org_url() # token
{
org_name=${user_name##*@}
org_xml=`api_org_get "$1"`
_scrap="${org_xml##*"$org_name\" href=\""}"
echo "${_scrap%%\"/>*}"
}

proc_get_network() # token
{

_url=`proc_get_org_url "$1"`
_xml=`url_get "$1" "$_url"`
_scrap="${_xml##*"ORG-EXT-R\" href=\""}"
echo "${_scrap%%\"/>*}"
}

proc_get_vdc() # token
{

_url=`proc_get_org_url "$1"`
_xml=`url_get "$1" "$_url"`
_scrap=`echo "$_xml" | grep "application/vnd.vmware.vcloud.vdc+xml\""`
_vdc="${_scrap##*"href=\""}"
echo "${_vdc%%\"/>*}"
}

proc_get_catalogue() # token
{
_url=`proc_get_org_url "$1"`
_xml=`url_get "$1" "$_url"`
_scrap=`echo "$_xml" | grep "application/vnd.vmware.vcloud.catalog+xml\""`
_cat="${_scrap##*"href=\""}"
echo "${_cat%%\"/>*}"
}

proc_get_image() # token
{
_cat_url=`proc_get_catalogue "$1"`
_xml=`url_get "$1" "$_cat_url"`
_scrap=`echo "$_xml" | grep -i "centos"`
_img="${_scrap##*"href=\""}"
echo "${_img%%\"/>*}"
}

proc_get_template() # token
{
_img=`proc_get_image "$1"`
_xml=`url_get "$1" "$_img"`
_scrap=`echo "$_xml" | grep "application/vnd.vmware.vcloud.vAppTemplate+xml\""`
_tmpl="${_scrap##*"href=\""}"
echo "${_tmpl%%\"/>*}"
}

proc_create_node() # token
{
# IP_MODE_VALS_1_5 = ['POOL', 'DHCP', 'MANUAL', 'NONE']
# Find network href/elem from org (look for:
# application/vnd.vmware.vcloud.orgNetwork+xml)

# Get VDC

# Send a "application/vnd.vmware.vcloud.instantiateVAppTemplateParams+xml"
# as a POST /vdc/{id}/action/instantiateVAppTemplate

# Retrieve task from vapp href
# Loop on get status from task

# POST /vApp/{id}/power/action/powerOn
vm_name="test-`tr -dc "[:alpha:]" < /dev/urandom | head -c 8`"
net_url=`proc_get_network "$1"`
vdc_url=`proc_get_vdc "$1"`
template_url=`proc_get_template "$1"`

CREATE_NODE_PAYLOAD=$(cat <<END_OF_XML
<InstantiateVAppTemplateParams name="$vm_name" xml:lang="en" xmlns="http://www.vmware.com/vcloud/v0.8" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
 <VAppTemplate href="$template_url" />
 <InstantiationParams>
  <ProductSection xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1" xmlns:q1="http://www.vmware.com/vcloud/v0.8">
   <Property ovf:key="password" ovf:value="q1W2e3R4t5Y6" xmlns="http://schemas.dmtf.org/ovf/envelope/1" />
  </ProductSection>
  <VirtualHardwareSection xmlns:q1="http://www.vmware.com/vcloud/v0.8">
   <Item xmlns="http://schemas.dmtf.org/ovf/envelope/1">
    <InstanceID xmlns="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData">1</InstanceID>
    <ResourceType xmlns="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData">3</ResourceType>
    <VirtualQuantity xmlns="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData">1</VirtualQuantity>
   </Item>
   <Item xmlns="http://schemas.dmtf.org/ovf/envelope/1">
    <InstanceID xmlns="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData">2</InstanceID>
    <ResourceType xmlns="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData">4</ResourceType>
    <VirtualQuantity xmlns="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData">1024</VirtualQuantity>
   </Item>
  </VirtualHardwareSection>
  <NetworkConfigSection>
   <NetworkConfig>
     <NetworkAssociation href="$net_url" />
   </NetworkConfig>
  </NetworkConfigSection>
 </InstantiationParams>
</InstantiateVAppTemplateParams>
END_OF_XML
)

curl --trace-ascii curl-trace.txt -i -k \
-H "Accept:application/*+xml;version="$host_api_version"" \
-H "Content-Type: application/vnd.vmware.vcloud.instantiateVAppTemplateParams+xml" \
-H "$1" -X POST \
"$vdc_url/action/instantiateVAppTemplate" \
-d "$CREATE_NODE_PAYLOAD"
#--data-urlencode $CREATE_NODE_PAYLOAD

echo "$vm_name"
}

# TODO: Add wait parameter to pause between creation and deletion
while test $# -gt 0
do
    case $1 in
        --settings )
            SETTINGS=$2
            shift
            ;;
        --help | -h )
            usage_and_exit 0
            ;;
        --version )
            version
            exit 0
            ;;
        -* )
            error "Unrecognised option: $1"
            ;;
        * )
            break
            ;;
    esac
    shift
done

CFG="$PARENT/../cloudhands-jasmin/cloudhands/jasmin/vcloud/$SETTINGS.cfg"
read_endpoint

if [ ! -n "$host_name" -a "$host_port" -a "$host_api_version" ]
then
    warning "Could not configure settings."
    exit $EXITCODE
else
    info "Endpoint settings configured."
fi

if [ `api_versions` = "0" ]
then
    warning "API is not responding"
    exit $EXITCODE
else
    info "$host_name contacted successfully."
fi

read_credentials

TOKEN=`api_login "$user_name" "$user_pass"`
info "Creating VM `proc_create_node "$TOKEN"`..."
exit $EXITCODE
