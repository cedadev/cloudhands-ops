#!/usr/bin/env python3
# encoding: UTF-8

import textwrap
import unittest

import cloudhands.ops.puppet

APPLIANCE_API_RESPONSE = """
{
    "info": {
        "page": {
            "url": "http://jasmin-cloud.jc.rl.ac.uk/appliance/b1d0fe9485074c079d2fc524275a949d", 
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
            ], 
            "uuid": "478aaa9c523c4e33b60ff3d9e5fd3a9d"
        }, 
        "item_02": {
            "account": "/users/bcumberbat", 
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
            ], 
            "uuid": "d7d927433b6849e4a76b6dd9d87f717f"
        }, 
        "item_03": {
            "_type": "directory", 
            "mount_path": "/group_workspaces/stfcloud/eumetsat/2014", 
            "_links": [
                [
                    "Public key", 
                    "canonical", 
                    "/resource/{}", 
                    33, 
                    "get", 
                    [], 
                    null
                ]
            ], 
            "uuid": "0dfe416064c649028bc2fdf66e227d0e", 
            "description": "Raw satellite data"
        }, 
        "item_04": {
            "_type": "directory", 
            "mount_path": "/group_workspaces/stfcloud/moum/scratch", 
            "_links": [
                [
                    "Public key", 
                    "canonical", 
                    "/resource/{}", 
                    34, 
                    "get", 
                    [], 
                    null
                ]
            ], 
            "uuid": "9848041e37964b449cd7949d12c42cf2", 
            "description": "Modelling data workspace"
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
        rv = list(cloudhands.ops.puppet.appliance_authorized_keys(
            APPLIANCE_API_RESPONSE))
        self.assertEqual(2, len(rv))
        self.assertIn(expected, rv)

    @unittest.skip("To be confirmed")
    def test_manifest_mount_point(self):
        expected = textwrap.dedent("""
            mount { 'http://jasmin-cloud.jc.rl.ac.uk/resource/33': 
              name        => '/group_workspaces/stfcloud/eumetsat/2014',
              ensure      => mounted,
              device      => ${::device},
              fstype      => 'panfs';
              options     => ${::options},
            }
        """)
        print(expected)
