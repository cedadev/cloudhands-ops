#!/bin/sh
if [ -z "$1" ]; then
    echo "No session id set" 1>&2;
    exit 1;
fi

if [ -z "$2" ]; then
    echo "No vApp id set" 1>&2;
    exit 1;
fi

curl -i --capath ./cloudclient/config/ca -X DELETE https://******.rl.ac.uk/api/vApp/$2 
