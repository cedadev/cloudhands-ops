#!/bin/sh
if [ -z "$1" ]; then
    echo "No session id set" 1>&2;
    exit 1;
fi

wget --server-response --ca-directory ./cloudclient/config/ca https://******.rl.ac.uk/api/org/ --header "x-vcloud-authorization: $1" -O org.xml
