import os
import sys

from .run import run
from .tools import tools
from .arguments import defaults_or_env, parse_args

def main():
    if os.path.basename(sys.argv[0]) == "eda-container-wrapper":
        tool, args, toolargs = parse_args()
    else:
        tool = sys.argv[0]
        args = defaults_or_env(tools[tool])
        toolargs = sys.argv[1:]

    sys.exit(run(tool, args, toolargs))

if __name__ == "__main__":
    main()
