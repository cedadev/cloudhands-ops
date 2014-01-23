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
echo `api_org_get "$TOKEN"`
exit $EXITCODE
