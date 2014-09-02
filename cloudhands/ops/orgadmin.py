#!/usr/bin/env python
# encoding: UTF-8

import argparse
import logging

from cloudhands.ops import __version__

__doc__ = """
.. program:: clpudhands-orgadmin

.. option:: --novenv

   Disables the creation of a fresh virtual environment.

.. option:: --nopep8

   Disables the PEP8 checks.

.. option:: --notest

   Disables the unit tests.

Eg::

    cloudhands-orgadmin --host=http://jasmin-cloud.jc.rl.ac.uk
"""

import execnet

DFLT_PORT = 22
DFLT_DB = ":memory:"

def multiplier(channel, factor):
    while not channel.isclosed():
        param = channel.receive()
        channel.send(param * factor)


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

    gw = execnet.makegateway()
    channel = gw.remote_exec(multiplier, factor=10)

    for i in range(5):
        channel.send(i)
        result = channel.receive()
        assert result == i * 10

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
        "--db", default=DFLT_DB,
        help="Set the path to the database [{}]".format(DFLT_DB))
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
    pass
