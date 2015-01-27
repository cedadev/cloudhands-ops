#!/usr/bin/env python
# encoding: UTF-8

from collections import namedtuple
from collections import OrderedDict
import json
import operator
import os.path
import re
import textwrap
import urllib


__doc__ = """

Puppet_ is a configuration management utility for Unix and Windows systems.
It has a declarative language to define the desired state of a host under
management. Such declarations are stored in files called `manifests`.

.. _Puppet: http://puppetlabs.com/

"""


class TypeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, type(re.compile(""))):
            return obj.pattern
            # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def appliance_authorized_keys(data:str):
    """
    This function consumes the data from the `Appliance` API endpoint to produce
    a manifest for Puppet. It extracts the public keys of Organisation members
    and generates a sshauthorizedkey_ directive for each one.

    .. _sshauthorizedkey: https://docs.puppetlabs.com/references/latest/type.html#sshauthorizedkey
    """
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

    jvo = next((i for i in tree.get("nav", {}).values()
            if i.get("_type", None) == "organisation"), None)
    choice = next((i for i in tree.get("items", {}).values()
            if i.get("_type", None) == "cataloguechoice"), None)

    if not (jvo and choice):
        raise StopIteration

    content = OrderedDict([
        ("hostname", "{}_{}".format(host, choice["template"])),
        ("type", choice["template"]),
        ("jvo", jvo["name"])])
    dirs = sorted((i for i in tree.get("items", {}).values()
            if i.get("_type", None) == "directory"),
            key=operator.methodcaller("get", "mount_path", None))
    for i in dirs:
        content[i["mount_path"]] = "${options}"
    return content
