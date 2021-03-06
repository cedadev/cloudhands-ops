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

from cloudhands.common.schema import Membership
from cloudhands.common.schema import Provider
from cloudhands.common.schema import Registration
from cloudhands.common.schema import Subscription
from cloudhands.common.schema import Touch
from cloudhands.common.schema import User

import cloudhands.ops.orgadmin


class OnboardingTests(unittest.TestCase):

    def setUp(self):
        self.session = Registry().connect(sqlite3, ":memory:").session
        initialise(self.session)

    def tearDown(self):
        Registry().disconnect(sqlite3, ":memory:")

    def test_user_new(self):
        rv = cloudhands.common.factories.user(self.session, "Test", "User")
        self.assertIsInstance(rv, User)
        user = self.session.merge(rv)
        self.assertEqual("Test", user.handle)
        self.assertEqual("User", user.surname)
        self.assertEqual(1, self.session.query(User).count())

    def test_user_create_existing(self):
        handle = "test"
        user = User(handle=handle, uuid=uuid.uuid4().hex)
        mine = user.uuid
        self.session.add(user)
        self.session.commit()

        rv = cloudhands.common.factories.user(self.session, "test")
        self.assertIsInstance(rv, User)
        user = self.session.merge(rv)
        self.assertEqual(1, self.session.query(User).count())
        self.assertEqual(mine, user.uuid)

    def test_subscription_new(self):
        version = "0.32"
        orgName = "test"
        public = "172.16.151.170/31"
        providers = [
            "cloudhands.jasmin.vcloud.phase04.cfg",
            "cloudhands.jasmin.amazon.ae40331.cfg",
        ]
        acts = []
        actions = cloudhands.ops.orgadmin.subscriptions(
            self.session, orgName, public, providers, version)
        while True:
            try:
                acts.append(next(actions))
            except StopIteration as final:
                self.assertTrue(
                    all(isinstance(i, Subscription) for i in final.value)
                )
                self.assertTrue(
                    all(i.provider.name in providers for i in final.value)
                )
                self.assertTrue(
                    all(i.organisation.name == orgName for i in final.value)
                )
                break

        self.assertEqual(6, len(acts))

        self.assertEqual(2, self.session.query(Subscription).count())
        self.assertEqual(2, self.session.query(Provider).count())

    def test_subscriptions_create_providers_exist(self):
        version = "0.32"
        orgName = "test"
        public = "172.16.151.170/31"
        providers = [
            "cloudhands.jasmin.vcloud.phase04.cfg",
            "cloudhands.jasmin.amazon.ae40331.cfg",
        ]
        for p in providers:
            self.session.add(Provider(
                name=p,
                uuid=uuid.uuid4().hex))
        self.session.commit()

        rv = list(cloudhands.ops.orgadmin.subscriptions(
            self.session, orgName, public, providers, version))
        self.assertEqual(2, len({i.artifact for i in rv}))
        self.assertTrue(all(isinstance(i.artifact, Subscription) for i in rv))
        self.assertTrue(all(i.artifact.provider.name in providers for i in rv))
        self.assertTrue(
            all(i.artifact.organisation.name == orgName for i in rv))

        self.assertEqual(2, self.session.query(Subscription).count())
        self.assertEqual(2, self.session.query(Provider).count())

    def test_subscriptions_create_existing(self):
        version = "0.32"
        orgName = "test"
        public = "172.16.151.170/31"
        providers = [
            "cloudhands.jasmin.vcloud.phase04.cfg",
            "cloudhands.jasmin.amazon.ae40331.cfg",
        ]
        self.assertTrue(list(cloudhands.ops.orgadmin.subscriptions(
            self.session, orgName, public, providers, version)))

        acts = []
        actions = cloudhands.ops.orgadmin.subscriptions(
            self.session, orgName, public, providers, version)
        while True:
            try:
                acts.append(next(actions))
            except StopIteration as final:
                self.assertTrue(
                    all(isinstance(i, Subscription) for i in final.value)
                )
                self.assertTrue(
                    all(i.provider.name in providers for i in final.value)
                )
                self.assertTrue(
                    all(i.organisation.name == orgName for i in final.value)
                )
                break

        self.assertEqual(0, len({i.artifact for i in acts}))

        self.assertEqual(2, self.session.query(Subscription).count())
        self.assertEqual(2, self.session.query(Provider).count())

    def test_membership_create(self):
        version = "0.32"
        orgName = "test"
        public = "172.16.151.170/31"
        providers = [
            "cloudhands.jasmin.vcloud.phase04.cfg",
            "cloudhands.jasmin.amazon.ae40331.cfg",
        ]
        acts = list(cloudhands.ops.orgadmin.subscriptions(
            self.session, orgName, public, providers, version))
        org = self.session.merge(acts[0].artifact.organisation)

        user = self.session.merge(
            cloudhands.common.factories.user(self.session, "test"))
        rv = cloudhands.ops.orgadmin.membership(
            self.session, user, org, version)
        self.assertIsInstance(rv, Membership)
        self.assertEqual(1, self.session.query(Membership).count())
        
    def test_registration_create_new(self):
        version = "0.32"
        email = "some.body@somewhere.net"
        user = self.session.merge(
            cloudhands.common.factories.user(self.session, "test"))
        reg = self.session.merge(cloudhands.common.factories.registration(
            self.session, user, email, version))
        self.assertIsInstance(reg, Registration)
        self.assertEqual(1, self.session.query(Registration).count())
        
    def test_registration_create_existing(self):
        version = "0.32"
        email = "some.body@somewhere.net"
        user = self.session.merge(
            cloudhands.common.factories.user(self.session, "test"))
        self.assertTrue(cloudhands.common.factories.registration(
            self.session, user, email, version))

        reg = cloudhands.common.factories.registration(
            self.session, user, email, version)
        self.assertIs(reg, None)
        self.assertEqual(1, self.session.query(Registration).count())

    def test_registration_create_new_email(self):
        version = "0.32"
        oldEmail = "some.body@somewhere.net"
        newEmail = "some.body@elsewhere.net"
        user = self.session.merge(
            cloudhands.common.factories.user(self.session, "test"))
        self.assertTrue(cloudhands.common.factories.registration(
            self.session, user, oldEmail, version))

        reg = cloudhands.common.factories.registration(
            self.session, user, newEmail, version)
        self.assertIsInstance(reg, Registration)
        self.assertEqual(2, self.session.query(Registration).count())

    def test_operation_via_cli(self):
        account = "somebody"
        surname = "Body"
        eMail = "some.body@somewhere.net"
        orgName = "test"
        public = "172.16.151.170/31"
        activator = "/root/bootstrap.sh"
        providers = [
            "cloudhands.jasmin.vcloud.phase04.cfg",
            "cloudhands.jasmin.amazon.ae40331.cfg",
        ]

        logFile = tempfile.NamedTemporaryFile()
        p = cloudhands.ops.orgadmin.parser()
        args = p.parse_args([
            "--account", account,
            "--email", eMail,
            "--surname", surname,
            "--organisation", orgName,
            "--public", public,
            "--activator", activator,
            "--providers", providers[0], providers[1],
            "--verbose",
            "--log", logFile.name])
        rv = cloudhands.ops.orgadmin.main(args)
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
