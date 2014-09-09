#!/usr/bin/env python
# encoding: UTF-8
__author__ = 'cl'

import urllib.request, base64, urllib.parse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

class vCloudHTTP(object):
    def login(url, username, password, version):
        request = urllib.request.Request(url + "/api/sessions")
        base64string = base64.b64encode(str(username+":"+password).encode('ascii'))
        request.add_header("Authorization", "Basic %s" % base64string.decode("utf-8"))
        request.add_header("Accept", "application/*+xml;version=" + str(version))
        request.get_method = lambda: 'POST'
        try:
            result = urllib.request.urlopen(request)
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            exit()
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            exit()
        else:
            res=(result.getheaders())
            auth=''.join(res[2]).replace("x-vcloud-authorization", "")
            return auth

    def httpGET(url, auth, version):
        request = urllib.request.Request(url)
        request.add_header("Accept", "application/*+xml;version=" + str(version))
        request.add_header("x-vcloud-authorization", auth)
        request.get_method = lambda: 'GET'
        try:
            response = urllib.request.urlopen(request)
        except HTTPError as e:
            print('Error stack trace: ', e.info(), e.geturl(), e.fp.read().decode('utf-8'))
            print('The server couldn\'t fulfill the request. The stack trace can be viewed above.')
            exit()
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            exit()
        else:
            XMLresponse=response.read().decode("utf-8")
            return XMLresponse

    def httpPOST(url, contenttype, auth, xml, version):
        request = urllib.request.Request(url)
        request.add_header("Accept", "application/*+xml;version=" + str(version))
        request.add_header("x-vcloud-authorization", auth)
        request.add_header("Content-Type", contenttype)
        request.get_method = lambda: 'POST'
        request.data = xml.encode('utf8')
        try:
            response = urllib.request.urlopen(request)
        except HTTPError as e:
            print (xml)
            print('Error stack trace: ', e.info(), e.geturl(), e.fp.read().decode('utf-8'))
            print('The server couldn\'t fulfill the request. The XML posted to the server and the stack trace can be viewed above.')
            print('Error code: ', e.code)
            exit()
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            exit()
        else:
            XMLresponse=response.read().decode("utf-8")
            return XMLresponse

    def httpDELETE(url, auth, version):
        request = urllib.request.Request(url)
        request.add_header("Accept", "application/*+xml;version=" + str(version))
        request.add_header("x-vcloud-authorization", auth)
        request.get_method = lambda: 'DELETE'
        try:
            response = urllib.request.urlopen(request)
        except HTTPError as e:
            print('Error stack trace: ', e.info(), e.geturl(), e.fp.read().decode('utf-8'))
            print('The server couldn\'t fulfill the request. The stack trace can be viewed above.')
            exit()
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            exit()
        else:
            XMLresponse=response.read().decode("utf-8")
            return XMLresponse
