#!/usr/bin/env python3
# encoding: UTF-8

import json
import textwrap
import unittest

import cloudhands.ops.puppet

APPLIANCE_API_RESPONSE = """
{
    "info": {
        "page": {
            "title": "Appliance parameters", 
            "url": "http://jasmin-cloud.jc.rl.ac.uk/appliance/b1d0fe9485074c079d2fc524275a949d"
        }, 
        "versions": {
            "cloudhands.jasmin": "0.50"
        }
    }, 
    "nav": {
        "nav_01": {
            "name": "EOSCloud",
            "_type": "organisation", 
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
            ]
        }
    }, 
    "items": {
        "item_01": {
            "uuid": "c9762dce02fd4af78e24f9df28845519", 
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
            "_type": "publickey", 
            "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAzDpup+XwRKfAq5PtDYrseifyOFqWeAra3rONBzfdKub0Aa2imNjNFk+Q1Eeoqfn92A9bTx024EzoCg7daIswbi+ynXtzda+DT1RnpKcuOyOt3Jy8413ZOd+Ks3AovBzCQPpALiNwPu5zieCvBrd9lD4BNZo4tG6ELIv9Qv+APXPheGdDIMzwkhOf/8och4YkFGcVeYhTCjOdO3sFF8WkFmdW/OJP87RH9FBHLWMirdTz4x2tT+Cyfe47NUYCmxRkdulexy71OSIZopZONYvwx3jmradjt2Hq4JubO6wbaiUbF+bvyMJapRIPE7+f37tTSDs8W19djRf7DEz7MANprbw== cl@eduserv.org.uk", 
            "account": "/root"
        }, 
        "item_02": {
            "uuid": "37323dfca0ab4b64b01aea1ee2a399b9", 
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
            "_type": "publickey", 
            "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAuOg/gIR9szQ0IcPjqD1jlY9enJETyppW39MAH0WV1LqR+/ULulG4uBUS/HBwvS7ggu3P6mj4i2hH9Kz9JGwnkuhxMJu3d/b/2Z7/1hBkQls5BKTzSoYnPCVYfvPyNXzRHEcRPjyfGcrIYz2CU4g5Ei2f0IgRngamDQrTU33QLosoaJqfw0pvX2SdFyFRmJkY6vH7j66ciXl2bfUUdf1KaoadkD+n59U6EiURrholSlaZp0gECjx0dM4mZUD0DqjWGll0NmnM4NIpCl+lTOrFLicJBgPuAnsrqp8HjGEHweRoPwFkKpcPkfyV+k0o/bltu3Lyd8KLJrVzYAUXRnLRpw== dehaynes@snow.badc.rl.ac.uk", 
            "account": "/users/bcumberbat"
        }, 
        "item_03": {
            "description": "Raw satellite data", 
            "mount_path": "/group_workspaces/stfcloud/eumetsat/2014", 
            "_type": "directory", 
            "uuid": "bf43217827ab4407adaef824a060bf1f", 
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
            ]
        }, 
        "item_04": {
            "description": "Modelling data workspace", 
            "mount_path": "/group_workspaces/stfcloud/moum/scratch", 
            "_type": "directory", 
            "uuid": "f8436e05546f4f149e2fc2842caf45c2", 
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
            ]
        }, 
        "item_05": {
            "purpose": "Headless VM for console access", 
            "uuid": "8de53b1202354413be3d39b57bf40e1d", 
            "template": "bastion_host", 
            "_links": [
                [
                    "Image", 
                    "canonical", 
                    "/resource/{}", 
                    102, 
                    "get", 
                    [], 
                    null
                ]
            ], 
            "_type": "cataloguechoice"
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

    def test_ini_mount_point(self):
        expected = {
            "hostname": "b1d0fe9485074c079d2fc524275a949d_bastion_host",
            "type": "bastion_host",
            "/group_workspaces/stfcloud/eumetsat/2014": "${options}",
            "/group_workspaces/stfcloud/moum/scratch": "${options}",
        }
        rv = cloudhands.ops.puppet.appliance_environment_variables(
            APPLIANCE_API_RESPONSE)
        self.assertTrue(set(expected.items()) <= set(rv.items()))

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
