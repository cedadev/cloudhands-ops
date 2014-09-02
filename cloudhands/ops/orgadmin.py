#!/usr/bin/env python
# encoding: UTF-8

__doc__ = """
cloudhands-orgadmin doc

.. program:: check.sh

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

def multiplier(channel, factor):
    while not channel.isclosed():
        param = channel.receive()
        channel.send(param * factor)

if __name__ == "__channelexec__":
    pass

if __name__ == "__main__":
    gw = execnet.makegateway()
    channel = gw.remote_exec(multiplier, factor=10)

    for i in range(5):
        channel.send(i)
        result = channel.receive()
        assert result == i * 10

    gw.exit()
