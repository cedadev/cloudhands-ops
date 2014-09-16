#!/usr/bin/env python
# encoding: UTF-8

import argparse
import datetime
import logging
import logging.handlers
import os.path
import platform
import sqlite3
import sys
import uuid

try:
    from cloudhands.ops import __version__
    import execnet
except ImportError:
    # Remote host
    __version__ = None

from cloudhands.common.connectors import initialise
from cloudhands.common.connectors import Registry
import cloudhands.common.factories
from cloudhands.common.schema import Component
from cloudhands.common.schema import EmailAddress
from cloudhands.common.schema import Membership
from cloudhands.common.schema import Organisation
from cloudhands.common.schema import Provider
from cloudhands.common.schema import Registration
from cloudhands.common.schema import Subscription
from cloudhands.common.schema import Touch
from cloudhands.common.schema import User
from cloudhands.common.states import MembershipState
from cloudhands.common.states import RegistrationState
from cloudhands.common.states import SubscriptionState


__doc__ = """

This command-line utility enables remote creation of Organisations and
Admin users. It makes changes to the cloudhands database.

eg::

    cloudhands-orgadmin \\
    --host=jasmin-cloud.jc.rl.ac.uk --identity=~/.ssh/id_rsa-jasminvm \\
    --db=/home/jasminuser/jasmin-web.sl3 \\
    --account=denderby \\
    --email=dominic.enderby@contractor.net \\
    --surname=enderby \\
    --organisation=STFCloud \\
    --activator=/root/bootstrap.sh \\
    --providers=cloudhands.jasmin.vcloud.phase04.cfg \
    cloudhands.jasmin.amazon.ae40331.cfg

Help for each option is printed on the command::

    cloudhands-orgadmin --help
"""

DFLT_PORT = 22
DFLT_DB = ":memory:"
DFLT_USER = "jasminuser"
DFLT_VENV = "jasmin-py3.3"

def subscriptions(session, orgName, providers, version):
    actor = session.merge(cloudhands.common.factories.component(
        session, handle="org.orgadmin"))
    maintenance = session.query(
        SubscriptionState).filter(
        SubscriptionState.name=="maintenance").one()

    org = session.query(Organisation).filter(
        Organisation.name == orgName).first()
    if not org:
        org = Organisation(
            uuid=uuid.uuid4().hex,
            name=orgName)
        session.add(org)

    for p in providers:
        provider = session.query(Provider).filter(
            Provider.name == p).first()
        if not provider:
            provider = Provider(
                name=p, uuid=uuid.uuid4().hex)
            session.add(provider)

        subs = session.query(Subscription).join(Organisation).join(
            Provider).filter(Organisation.id==org.id).filter(
            Provider.id==provider.id).first()
        if subs:
            yield subs
        else:

            subs = Subscription(
                uuid=uuid.uuid4().hex,
                model=version,
                organisation=org,
                provider=provider)
            act = Touch(
                artifact=subs, actor=actor, state=maintenance,
                at=datetime.datetime.utcnow())

            session.add(act)
            session.commit()

            yield subs


def membership(session, user, org, version, role="admin"):
    actor = session.merge(cloudhands.common.factories.component(
        session, handle="org.orgadmin"))
    created = session.query(MembershipState).filter(
        MembershipState.name == "created").one()
    mship = Membership(
        uuid=uuid.uuid4().hex,
        model=version,
        organisation=org,
        role=role)
    acts = (
        Touch(artifact=mship, actor=actor, state=created,
                at=datetime.datetime.utcnow()),
        Touch(artifact=mship, actor=user, state=created,
                at=datetime.datetime.utcnow())
    )
    session.add_all(acts)
    session.commit()
    return mship


def main(args):
    log = logging.getLogger("cloudhands.ops.orgadmin")

    log.setLevel(args.log_level)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-7s %(name)s|%(message)s")
    ch = logging.StreamHandler()

    if args.log_path is None:
        ch.setLevel(args.log_level)
    else:
        fh = logging.handlers.WatchedFileHandler(args.log_path)
        fh.setLevel(args.log_level)
        fh.setFormatter(formatter)
        log.addHandler(fh)
        ch.setLevel(logging.WARNING)

    ch.setFormatter(formatter)
    log.addHandler(ch)

    if not args.host:
        log.debug("Executing locally.")
        s = "popen//dont_write_bytecode"
    else:
        s = ("ssh=-i {identity} -p {0.port} {0.user}@{0.host}"
            "//python=/home/{0.user}/{0.venv}/bin/python").format(
            args,
            identity=os.path.expanduser(args.identity))

    gw = execnet.makegateway(s)
    try:
        ch = gw.remote_exec(sys.modules[__name__])
        data = vars(args)
        data["__version__"] = __version__
        log.debug("Supplying args {}.".format(data))
        ch.send(data)

        msg = ch.receive()
        while msg is not None:
            log.info(msg)
            msg = ch.receive()

    except OSError as e:
        log.error(s)
        log.error(e)
    finally:
        gw.exit()
    return 0


def parser(description=__doc__):
    rv = argparse.ArgumentParser(
        description,
        fromfile_prefix_chars="@"
    )
    rv.add_argument(
        "--host", required=False,
        help="Specify the name of the database host")
    rv.add_argument(
        "--port", type=int, default=DFLT_PORT,
        help="Specify the port number [{}] to the host".format(DFLT_PORT))
    rv.add_argument(
        "--user", default=DFLT_USER,
        help="Specify the user login [{}] on the host".format(DFLT_USER))
    rv.add_argument(
        "--venv", default=DFLT_VENV,
        help="Specify the Python environment [{}] on the host".format(
            DFLT_VENV)
        )
    rv.add_argument(
        "--db", default=DFLT_DB,
        help="Specify the path to the database [{}] on the host".format(DFLT_DB))
    rv.add_argument(
        "--identity", default="",
        help="Specify the path to a SSH public key authorised on the host")

    rv.add_argument(
        "--account", required=True,
        help="Set the account name for the administrator")
    rv.add_argument(
        "--email", required=True,
        help="Set the email address of the administrator")
    rv.add_argument(
        "--surname", required=True,
        help="Set the surname of the administrator")
    rv.add_argument(
        "--organisation", required=True,
        help="Set the name of the organisation to be created")
    rv.add_argument(
        "--activator", required=True,
        help="Specify the path to the appliance activator script.")
    rv.add_argument(
        "--providers", nargs="+", required=True,
        help="Set one or more subscribed providers")
    rv.add_argument(
        "--public", nargs="+",
        help="Specify one or more public IP addresses")

    rv.add_argument(
        "--version", action="store_true", default=False,
        help="Print the current version number")
    rv.add_argument(
        "-v", "--verbose", required=False,
        action="store_const", dest="log_level",
        const=logging.DEBUG, default=logging.INFO,
        help="Increase the verbosity of output")
    rv.add_argument(
        "--log", default=None, dest="log_path",
        help="Specify a file path for log output")
    return rv


def run():
    p = parser()
    args = p.parse_args()
    if args.version:
        sys.stdout.write(__version__ + "\n")
        rv = 0
    else:
        rv = main(args)
    sys.exit(rv)

if __name__ == "__main__":
    run()

if __name__ == "__channelexec__":
    channel.send("Sending from {}.".format(platform.node()))

    args = channel.receive()

    session = Registry().connect(sqlite3, args["db"]).session
    initialise(session)

    admin = cloudhands.common.factories.user(
        session, args["account"], args["surname"])
    channel.send((admin.typ, admin.handle, admin.uuid))

    org = None
    for subs in subscriptions(
        session, args["organisation"], args["providers"], args["version"]
    ):
        org = session.merge(subs.organisation)
        channel.send(("provider", subs.provider.name, subs.provider.uuid))
        channel.send((subs.typ, subs.uuid))

    channel.send(("organisation", org.name, org.uuid))

    mship = membership(session, admin, org, args["version"])
    channel.send((mship.typ, mship.role, mship.uuid))

    reg = cloudhands.common.factories.registration(
        session, admin, args["email"], args["version"])
    if reg is not None:
        channel.send((reg.typ, reg.uuid))

    channel.send(None)
