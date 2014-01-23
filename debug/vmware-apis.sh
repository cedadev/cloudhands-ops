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
CFG="$PARENT/../cloudhands-jasmin/cloudhands/jasmin/vcloud/phase01.cfg"

error()
{
    echo "$@" 1>&2
    usage_and_exit 1
}

usage()
{
    echo "Usage: $PROGRAM [--user USER]"
}

usage_and_exit()
{
    usage
    exit "$1"
}

version()
{
    VERSION=$(head "$PARENT/cloudhands/ops/__init__.py" | cut -d= -f2 | tr -d '" ')
    echo "$PROGRAM $VERSION"
}

warning()
{
    echo "$@" 1>&2
    EXITCODE=$(($EXITCODE + 1))
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

read -r -d '' TEST_LOGIN <<'END'
HTTP/1.1 200 OK
Date: Tue, 14 Jan 2014 10:58:48 GMT
x-vcloud-authorization: TF6QoPX2xZbwVZM0yT4QmMfM6nKvC2Yz/HqkuFdpU0U=
Set-Cookie: vcloud-token=TF6QoPX2xZbwVZM0yT4QmMfM6nKvC2Yz/HqkuFdpU0U=; Secure;
Path=/
Content-Type: application/vnd.vmware.vcloud.session+xml;version=1.5
Date: Tue, 14 Jan 2014 10:58:48 GMT
Content-Length: 884

<?xml version="1.0" encoding="UTF-8"?>
<Session xmlns="http://www.vmware.com/vcloud/v1.5" user="dehaynes"
org="CEMSTest" type="application/vnd.vmware.vcloud.session+xml"
href="https://vcloud.cems.rl.ac.uk/api/session/"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.vmware.com/vcloud/v1.5
http://vcloud.cems.rl.ac.uk/api/v1.5/schema/master.xsd">
  <Link rel="down" type="application/vnd.vmware.vcloud.orgList+xml"
href="https://vcloud.cems.rl.ac.uk/api/org/"/>
  <Link rel="down" type="application/vnd.vmware.admin.vcloud+xml"
href="https://vcloud.cems.rl.ac.uk/api/admin/"/>
  <Link rel="down" type="application/vnd.vmware.vcloud.query.queryList+xml"
href="https://vcloud.cems.rl.ac.uk/api/query"/>
  <Link rel="entityResolver" type="application/vnd.vmware.vcloud.entity+xml"
href="https://vcloud.cems.rl.ac.uk/api/entity/"/>
</Session>
END

api_login()
{
    TOKEN=`curl -s -i -k -u 'dehaynes@CEMSTest:#########' \
    -H 'Accept:application/*+xml;version=1.5' -X POST  \
    https://cemscloud.jc.rl.ac.uk:443/api/sessions \
    | grep 'x-vcloud-authorization.*'`
}

while test $# -gt 0
do
    case $1 in
        --user )
            USER=$2
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
    exit 0
else
    echo "API is responding"
fi
read_credentials
echo $user_name
echo $user_pass
api_login
echo $TOKEN
warning "That's your lot, $USER!"
