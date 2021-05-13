import argparse
import os
import sys

from .run import run, RunArguments, RunArgumentsDefaults, tools

def main():
    if os.path.basename(sys.argv[0]) == "eda-container-wrapper":
        parser = argparse.ArgumentParser()
        parser.add_argument('--split-cwd-tail', type=int, default=RunArgumentsDefaults.split_cwd_tail)
        parser.add_argument('--tool-version')
        parser.add_argument('--non-interactive', action="store_true")
        parser.add_argument('tool', choices=tools.keys())
        parser.add_argument('toolargs', nargs='*')
        args = parser.parse_args()
        tool = args.tool
        toolargs = args.toolargs
        args = RunArguments(
            split_cwd_tail = args.split_cwd_tail,
            tool_version = args.tool_version if args.tool_version else tools[tool].default_version,
            interactive = not args.non_interactive
        )
    else:
        tool = sys.argv[0]
        args = RunArguments(split_cwd_tail=0, interactive=True)
        toolargs = sys.argv[1:]

    run(tool, args, toolargs)

if __name__ == "__main__":
    main()
