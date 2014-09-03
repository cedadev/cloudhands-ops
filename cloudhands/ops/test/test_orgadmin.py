#!/usr/bin/env python3
# encoding: UTF-8

import datetime
import sqlite3
import unittest
import uuid

from cloudhands.common.connectors import initialise
from cloudhands.common.connectors import Registry


class OnboardingTests(unittest.TestCase):

    def setUp(self):
        self.session = Registry().connect(sqlite3, ":memory:").session
        initialise(self.session)

    def tearDown(self):
        Registry().disconnect(sqlite3, ":memory:")

    def test_user_create(self):
        self.fail("Unimplemented")

    def test_organisation_create(self):
        self.fail("Unimplemented")

    def test_membership_create(self):
        self.fail("Unimplemented")
