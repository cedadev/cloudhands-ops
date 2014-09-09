#!/usr/bin/env python
# encoding: UTF-8
__author__ = 'cl'

import unittest
import parse_yaml
import yaml

class RegexTest(unittest.TestCase):

    def test_vcenter_object(self):
        fragment = yaml.safe_load("""
connectionstrings:
  vcenter:
    hostname: vcenter.example.com
    username: testuser
    password: testpassword
        """)
        self.assertEqual("vcenter.example.com", parse_yaml.evaluateData(fragment, "vcenter", "prod").Hostname)

    def test_host_object(self):
        fragment = yaml.safe_load("""
configuration:
  esxi:
    name: esx
    domain: .example.com
    storageNet: 10.0.0.0/20
    vxlanNet: 172.0.0.0/18
clusters:
  rack3-1:
    storageGW: 10.0.0.1
    vxlanGW: 172.0.0.1
    hostrange:
    - 050-073
    - 100-150
        """)
        print(parse_yaml.evaluateData(fragment, "host", "070").FullName)
        self.assertEqual("esx070.example.com", parse_yaml.evaluateData(fragment, "host", "070").FullName)

    def test_cluster_object(self):
        fragment = yaml.safe_load("""
clusters:
  rack3-1:
    storageGW: 10.0.0.1
    vxlanGW: 172.0.0.1
    hostrange:
    - 050-073
    - 100-150
        """)
        self.assertEqual("rack3-1", parse_yaml.evaluateData(fragment, "cluster", "rack3-1").Name)

if __name__ == "__main__":
   unittest.main()

