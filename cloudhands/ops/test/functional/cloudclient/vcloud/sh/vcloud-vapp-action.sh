#!/bin/sh
if [ -z "$1" ]; then
    echo "No session id set" 1>&2;
    exit 1;
fi

if [ -z "$2" ]; then
    echo "No vApp id set" 1>&2;
    exit 1;
fi

if [ -z "$3" ]; then
    echo "No action set for vApp e.g. \"power/action/powerOff\"" 1>&2;
    exit 1;
fi

wget --server-response --ca-directory ./cloudclient/config/ca https://******.rl.ac.uk/api/vApp/$2/$3 --header "x-vcloud-authorization: $1" --post-data='' -O $2-action-$(basename $3).xml
