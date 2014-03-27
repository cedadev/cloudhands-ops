#!/usr/bin/env python
#   encoding: UTF-8

from collections import Counter
import os.path
import subprocess
import sys

from radon.cli import iter_filenames 
from radon.raw import analyze

def build_stats(parent, proj):
    cntr = Counter()
    path = os.path.abspath(os.path.join(parent, proj))
    for fP in iter_filenames([path], exclude="*setup.py"):
        with open(fP, 'r') as fObj:
            sys.stderr.write("analyzing {}\n".format(fP))
            mod = analyze(fObj.read())
            cntr.update(vars(mod))

    rel = subprocess.check_output(
        [sys.executable, "setup.py", "--version"],
        cwd=path).decode("utf-8").strip()
    return (proj, rel, cntr["lloc"])

if __name__ == "__main__":
    args = iter(sys.argv)
    prog = next(args)
    parent = next(args)
    projs = list(args)
    sys.stdout.write(
        "\n".join("{: >18}\t{}\t{}".format(*build_stats(parent, proj))
        for proj in projs))
    sys.stdout.write("\n")
