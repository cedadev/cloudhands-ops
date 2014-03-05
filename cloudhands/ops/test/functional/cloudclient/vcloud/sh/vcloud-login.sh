#!/bin/bash 
if [ -z "$1" ]; then
    echo "No hostname set" 1>&2;
    exit 1;
fi
if [ -z "$2" ]; then
    echo "No user id set" 1>&2;
    exit 1;
fi

curl -X POST https://$1/api/sessions --user $2 -k -H 'Accept:application/*+xml;version=1.5' -i
