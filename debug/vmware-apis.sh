#! /bin/sh -

# This boilerplate from 'Classic Shell Scripting'

IFS='
    '
OLDPATH="$PATH"
PATH="/bin:/usr/bin"
export PATH

EXITCODE=0
PROGRAM=$( basename "$0" )

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
    DIR=$( cd "$( dirname "$0" )" && pwd )
    PARENT=$(readlink -e "$DIR/..")
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

warning "That's your lot, $USER!"
