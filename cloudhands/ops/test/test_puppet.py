#!/usr/bin/env python3
# encoding: UTF-8

import textwrap
import unittest

import cloudhands.ops.puppet

APPLIANCE_API_RESPONSE = """
{
    "info": {
        "page": {
            "url":
"http://jasmin-cloud.jc.rl.ac.uk/appliance/b1d0fe9485074c079d2fc524275a949d", 
            "title": "Appliance parameters"
        }, 
        "versions": {
            "cloudhands.jasmin": "0.50"
        }
    }, 
    "nav": {
        "nav_01": {
            "_links": [
                [
                    "EOSCloud", 
                    "up", 
                    "/organisation/{}", 
                    "EOSCloud", 
                    "get", 
                    [], 
                    null
                ]
            ], 
            "name": "EOSCloud"
        }
    }, 
    "items": {
        "item_01": {
            "account": "/root", 
            "uuid": "3cae46c2458f459fbd759d7a77617372", 
            "_type": "publickey", 
            "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAzDpup+XwRKfAq5PtDYrseifyOFqWeAra3rONBzfdKub0Aa2imNjNFk+Q1Eeoqfn92A9bTx024EzoCg7daIswbi+ynXtzda+DT1RnpKcuOyOt3Jy8413ZOd+Ks3AovBzCQPpALiNwPu5zieCvBrd9lD4BNZo4tG6ELIv9Qv+APXPheGdDIMzwkhOf/8och4YkFGcVeYhTCjOdO3sFF8WkFmdW/OJP87RH9FBHLWMirdTz4x2tT+Cyfe47NUYCmxRkdulexy71OSIZopZONYvwx3jmradjt2Hq4JubO6wbaiUbF+bvyMJapRIPE7+f37tTSDs8W19djRf7DEz7MANprbw== cl@eduserv.org.uk", 
            "_links": [
                [
                    "Public key", 
                    "canonical", 
                    "/resource/{}", 
                    12, 
                    "get", 
                    [], 
                    null
                ]
            ]
        }, 
        "item_02": {
            "account": "/users/bcumberbat", 
            "uuid": "5b1c13ca375246929967927e6f39fc7f", 
            "_type": "publickey", 
            "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAuOg/gIR9szQ0IcPjqD1jlY9enJETyppW39MAH0WV1LqR+/ULulG4uBUS/HBwvS7ggu3P6mj4i2hH9Kz9JGwnkuhxMJu3d/b/2Z7/1hBkQls5BKTzSoYnPCVYfvPyNXzRHEcRPjyfGcrIYz2CU4g5Ei2f0IgRngamDQrTU33QLosoaJqfw0pvX2SdFyFRmJkY6vH7j66ciXl2bfUUdf1KaoadkD+n59U6EiURrholSlaZp0gECjx0dM4mZUD0DqjWGll0NmnM4NIpCl+lTOrFLicJBgPuAnsrqp8HjGEHweRoPwFkKpcPkfyV+k0o/bltu3Lyd8KLJrVzYAUXRnLRpw== dehaynes@snow.badc.rl.ac.uk", 
            "_links": [
                [
                    "Public key", 
                    "canonical", 
                    "/resource/{}", 
                    54, 
                    "get", 
                    [], 
                    null
                ]
            ]
        }, 
        "item_03": {
            "mount_path": "/group_workspaces/stfcloud/eumetsat/2014", 
            "description": "Raw satellite data", 
            "_type": "directory", 
            "uuid": "f7c5092d2b3440a48c40f486b153f929"
        }, 
        "item_04": {
            "mount_path": "/group_workspaces/stfcloud/moum/scratch", 
            "description": "Modelling data workspace", 
            "_type": "directory", 
            "uuid": "2bbf4fbfb1cd4cfb8a725fd5c4ca5751"
        }
    }, 
    "options": {}
}
"""

class FormattingTests(unittest.TestCase):

    def test_manifest_sshkey(self):
        expected = textwrap.dedent("""
            ssh_authorized_key { 'http://jasmin-cloud.jc.rl.ac.uk/resource/54': 
              name     => 'dehaynes@snow.badc.rl.ac.uk',
              ensure   => present,
              key      => 'AAAAB3NzaC1yc2EAAAABIwAAAQEAuOg/gIR9szQ0IcPjqD1jlY9enJETyppW39MAH0WV1LqR+/ULulG4uBUS/HBwvS7ggu3P6mj4i2hH9Kz9JGwnkuhxMJu3d/b/2Z7/1hBkQls5BKTzSoYnPCVYfvPyNXzRHEcRPjyfGcrIYz2CU4g5Ei2f0IgRngamDQrTU33QLosoaJqfw0pvX2SdFyFRmJkY6vH7j66ciXl2bfUUdf1KaoadkD+n59U6EiURrholSlaZp0gECjx0dM4mZUD0DqjWGll0NmnM4NIpCl+lTOrFLicJBgPuAnsrqp8HjGEHweRoPwFkKpcPkfyV+k0o/bltu3Lyd8KLJrVzYAUXRnLRpw==',
              type     => 'ssh-rsa',
              user     => 'bcumberbat',
            }
        """)
        print(expected)
