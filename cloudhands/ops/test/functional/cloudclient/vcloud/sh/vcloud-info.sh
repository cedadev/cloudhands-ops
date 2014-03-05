#!/bin/sh

curl -X GET $1 \
	-H "x-vcloud-authorization: $2" \
	-H 'Accept: application/*+xml;version=1.5' \
	--insecure
