!#/bin/sh
if [ -z "$1" ]; then
    echo "No session id set" 1>&2;
    exit 1;
fi

if [ -z "$2" ]; then
    echo "No vApp id set" 1>&2;
    exit 1;
fi

wget --server-response --ca-directory ./cloudclient/config/ca https://******.rl.ac.uk/api/vApp/$2 --header "x-vcloud-authorization: $1" -O vapp-info-$2.xml
