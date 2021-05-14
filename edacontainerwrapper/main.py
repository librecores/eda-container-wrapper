import argparse
import os
import sys

from .run import run
from .tools import tools
from .arguments import defaults_or_env, parse_args, RunArguments

def write_wrapper(tool, path, args):
    with open(path, "w") as f:
        f.write("#!/usr/bin/env python3\n\n")
        f.write("import sys\n")
        f.write("from edacontainerwrapper.arguments import defaults_or_env, RunArguments\n")
        f.write("from edacontainerwrapper.run import run\n\n")
        f.write("from edacontainerwrapper.tools import tools\n\n")
        f.write("if __name__ == '__main__':\n")
        f.write(f"\targs = defaults_or_env(tools['{tool}'], {str(args)})\n\n")
        f.write(f"\tsys.exit(run('{tool}', args, sys.argv[1:]))\n")


def main():
    if os.path.basename(sys.argv[0]) == "eda-container-wrapper":
        tool, write_script, args, toolargs = parse_args()
        if write_script:
            return write_wrapper(tool, write_script, args)
    else:
        tool = sys.argv[0]
        args = defaults_or_env(tools[tool])
        toolargs = sys.argv[1:]

    sys.exit(run(tool, args, toolargs))

if __name__ == "__main__":
    main()
