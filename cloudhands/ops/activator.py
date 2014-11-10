#!/usr/bin/env python
# encoding: UTF-8

import argparse
from collections import namedtuple
from collections import OrderedDict
import json
import logging
import logging.handlers
import operator
import os.path
import platform
import sys
import textwrap
import urllib
import uuid

try:
    from cloudhands.ops import __version__
except ImportError:
    __version__ = None


__doc__ = """

Functions which produce puppet manifest entries from web API data.

"""

DFLT_PORT = 22
DFLT_USER = "jasminportal"
DFLT_VENV = "jasmin-py3.3"

def appliance_authorized_keys(data):
    Key = namedtuple("Key", ["type", "value", "name"])
    tmplt = textwrap.dedent("""
    ssh_authorized_key {{ '{parent.scheme}://{parent.netloc}{path}': 
      name     => '{key.name}',
      ensure   => present,
      key      => '{key.value}',
      type     => '{key.type}',
      user     => '{user}',
    }}
    """)
    tree = json.loads(data)
    try:
        url = tree["info"]["page"]["url"]
    except KeyError:
        raise StopIteration
    else:
        host = urllib.parse.urlparse(url)

    objs = (i for i in tree.get("items", {}).values()
            if i.get("_type", None) == "publickey")
    for obj in objs:
        key = Key(*obj["public_key"].split(None, 2))
        user = obj["account"].split("/")[-1]
        link = next((i for i in obj.get("_links", [])
                    if i[1] == "canonical"), None)
        yield tmplt.format(
            user=user, key=key, parent=host, path=link[2].format(link[3]))
        
def appliance_environment_variables(data):
    tree = json.loads(data)
    try:
        url = tree["info"]["page"]["url"]
    except KeyError:
        raise StopIteration
    else:
        host = urllib.parse.urlparse(url).path.split('/')[-1]

    choice = next((i for i in tree.get("items", {}).values()
            if i.get("_type", None) == "cataloguechoice"), None)
    content = OrderedDict([
        ("hostname", "{}_{}".format(host, choice["template"])),
        ("type", choice["template"])])
    dirs = sorted((i for i in tree.get("items", {}).values()
            if i.get("_type", None) == "directory"),
            key=operator.methodcaller("get", "mount_path", None))
    for i in dirs:
        content[i["mount_path"]] = "${options}"
    return "\n".join("{}: {}".format(k, v) for k, v in content.items())

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
        "--identity", default="",
        help="Specify the path to a SSH public key authorised on the host")


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
