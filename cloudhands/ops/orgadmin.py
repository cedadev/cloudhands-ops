#!/usr/bin/env python
# encoding: UTF-8

import argparse
import logging
import os.path
import platform
import sys

try:
    from cloudhands.ops import __version__
    import execnet
except ImportError:
    # Remote host
    __version__ = None

__doc__ = """

This command-line utility enables remote creation of Organisations and
Admin users. It makes changes to the cloudhands database.

eg::

    cloudhands-orgadmin \
    --host=jasmin-cloud.jc.rl.ac.uk --identity=~/.ssh/id_rsa-jasminvm.pub

Help for each option is printed on the command::

    cloudhands-orgadmin --help
"""

DFLT_PORT = 22
DFLT_DB = ":memory:"
DFLT_USER = "jasminuser"
DFLT_VENV = "jasmin-py3.3"

def main(args):
    log = logging.getLogger("cloudhands.ops")

    log.setLevel(args.log_level)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-7s %(name)s|%(message)s")
    ch = logging.StreamHandler()

    if args.log_path is None:
        ch.setLevel(args.log_level)
    else:
        fh = WatchedFileHandler(args.log_path)
        fh.setLevel(args.log_level)
        fh.setFormatter(formatter)
        log.addHandler(fh)
        ch.setLevel(logging.WARNING)

    ch.setFormatter(formatter)
    log.addHandler(ch)

    s = ("ssh=-i {identity} -p {0.port} {0.user}@{0.host}"
        "//python=/home/{0.user}/{0.venv}/bin/python").format(
        args,
        identity=os.path.expanduser(args.identity))
    gw = execnet.makegateway(s)
    try:
        ch = gw.remote_exec(sys.modules[__name__])
        ch.send(vars(args))

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
    rv = argparse.ArgumentParser(description)
    rv.add_argument(
        "--version", action="store_true", default=False,
        help="Print the current version number")
    rv.add_argument(
        "-v", "--verbose", required=False,
        action="store_const", dest="log_level",
        const=logging.DEBUG, default=logging.INFO,
        help="Increase the verbosity of output")
    rv.add_argument(
        "--host", required=True,
        help="Specify the name of the database host")
    rv.add_argument(
        "--port", type=int, default=DFLT_PORT,
        help="Set the port number [{}]".format(DFLT_PORT))
    rv.add_argument(
        "--user", default=DFLT_USER,
        help="Specify the login user [{}]".format(DFLT_USER))
    rv.add_argument(
        "--venv", default=DFLT_VENV,
        help="Specify the Python environment on the remote host [{}]".format(
            DFLT_VENV)
        )
    rv.add_argument(
        "--db", default=DFLT_DB,
        help="Set the path to the database [{}]".format(DFLT_DB))
    rv.add_argument(
        "--identity", default="",
        help="Specify the path to an SSH public key file")
    rv.add_argument(
        "--log", default=None, dest="log_path",
        help="Set a file path for log output")
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
    channel.send("Executing remotely from {}.".format(platform.node()))
    args = channel.receive()
    channel.send("Received args {}.".format(args))
    channel.send(None)
