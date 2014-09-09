#!/usr/bin/env python
# encoding: UTF-8
import sys

import cloudhands.ops.scripts.parse_yaml as p

hostNum = str(sys.argv[1])
cmd = sys.argv[2]

print(p.ExecCommand(hostNum, cmd))
