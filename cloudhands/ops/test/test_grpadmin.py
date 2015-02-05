#!/usr/bin/env python3
# encoding: UTF-8

import datetime
import sqlite3
import tempfile
import unittest
import uuid

from cloudhands.common.connectors import initialise
from cloudhands.common.connectors import Registry

import cloudhands.common.factories

from cloudhands.common.schema import Access
from cloudhands.common.schema import Provider
from cloudhands.common.schema import Registration
from cloudhands.common.schema import Subscription
from cloudhands.common.schema import Touch
from cloudhands.common.schema import User

import cloudhands.ops.grpadmin


class OnboardingTests(unittest.TestCase):

    def setUp(self):
        self.session = Registry().connect(sqlite3, ":memory:").session
        initialise(self.session)

    def tearDown(self):
        Registry().disconnect(sqlite3, ":memory:")

    def test_access_create(self):
        version = "0.32"
        orgName = "test"
        public = "172.16.151.170/31"

        user = self.session.merge(
            cloudhands.common.factories.user(self.session, "test"))
        group = self.session.merge(
            cloudhands.common.factories.group(self.session, "test", 1234))
        rv = cloudhands.ops.grpadmin.access(
            self.session, user, group, version)
        self.assertIsInstance(rv, Access)
        self.assertEqual(1, self.session.query(Access).count())
        
    def test_operation_via_cli(self):
        account = "somebody"
        surname = "Body"
        eMail = "some.body@somewhere.net"
        grpName = "test"
        grpNumber = 12345

        logFile = tempfile.NamedTemporaryFile()
        p = cloudhands.ops.grpadmin.parser()
        args = p.parse_args([
            "--account", account,
            "--email", eMail,
            "--surname", surname,
            "--group", grpName,
            "--number", grpNumber,
            "--verbose",
            "--log", logFile.name])
        rv = cloudhands.ops.grpadmin.main(args)
        outFile = open(logFile.name, 'r')
        lines = outFile.readlines()
        contents = iter(lines)
        self.assertTrue("Executing locally" in next(contents))
        self.assertTrue("Supplying args" in next(contents))
        self.assertTrue("Sending from" in next(contents))
        self.assertTrue("user" in next(contents))
        self.assertTrue("provider" in next(contents))
        self.assertTrue("subscription" in next(contents))
        self.assertTrue("provider" in next(contents))
        self.assertTrue("subscription" in next(contents))
        self.assertTrue("organisation" in next(contents))
        self.assertTrue("membership" in next(contents))
        self.assertTrue("registration" in next(contents))
        outFile.close()
        logFile.close()
