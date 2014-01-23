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
CFG="$PARENT/../cloudhands-jasmin/cloudhands/jasmin/vcloud/$SETTINGS.cfg"

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

api_versions()
{
    REPLY=`curl -s -k -H 'Accept:application/*+xml;version=1.5' -X GET \
https://cemscloud.jc.rl.ac.uk:443/api/versions`
    echo $REPLY | tr ' ' '\n' | grep -E -o "v[[:digit:]]*\.[[:digit:]]*" \
    | sort | uniq | wc -l
}

read_credentials()
{
    # Read the variables 'name' and 'pass' from the user section of a config
    # file
    if [ -f "$CFG" ]
    then
        while read -r key value; do
            eval user_$key=\$value
        done < <(grep -A2 '\[user\]' $CFG \
                | tr -d ' ' | cut -s -d'=' -f1,2 --output-delimiter=" ")
    else
        warning "Could not find settings ($CFG)"
        exit 0
    fi
}

api_login()
{
    curl -s -i -k -u "$1:$2" \
    -H 'Accept:application/*+xml;version=1.5' -X POST  \
    https://cemscloud.jc.rl.ac.uk:443/api/sessions \
    | grep 'x-vcloud-authorization.*'
}

api_org_get()
{
    curl -s -i -k -H 'Accept:application/*+xml;version=1.5' \
    -H "$1" \
    -X GET https://cemscloud.jc.rl.ac.uk:443/api/org
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


if [ `api_versions` = "0" ]
then
    warning "API is not responding"
    exit $EXITCODE
else
    info "Endpoint contacted successfully."
fi

read_credentials
TOKEN=`api_login "$user_name" "$user_pass"`
echo `api_org_get "$TOKEN"`
exit $EXITCODE
