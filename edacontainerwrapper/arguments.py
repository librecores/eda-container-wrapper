import argparse
from collections import namedtuple
import os

from .tools import tools
from .version import version

RunArguments = namedtuple("RunArguments", "split_cwd_tail tool_version interactive cwd_base")

def defaults_or_env(tool=None, defaults=None):
    if not defaults:
        defaults = RunArguments(
            split_cwd_tail = 0,
            tool_version = None,
            interactive = True,
            cwd_base = None
        )
    return RunArguments(
        split_cwd_tail = os.getenv("ECW_SPLIT_CWD_TAIL", default=defaults.split_cwd_tail),
        tool_version = os.getenv("ECW_TOOL_VERSION", default=tool.default_version if tool else defaults.tool_version),
        interactive = os.getenv("ECW_INTERACTIVE", default="True" if defaults.interactive else "False").lower() in ("true", "1"),
        cwd_base = os.getenv("ECW_CWD_BASE", default=defaults.cwd_base),
    )

def parse_args():
    defargs = defaults_or_env()
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-script')
    parser.add_argument('--split-cwd-tail', type=int, default=defargs.split_cwd_tail)
    parser.add_argument('--cwd-base', default=defargs.cwd_base)
    parser.add_argument('--tool-version')
    parser.add_argument('--non-interactive', action="store_true", default=not defargs.interactive)
    parser.add_argument('--version', action='version', version=version)
    parser.add_argument('tool', choices=tools.keys())
    parser.add_argument('toolargs', nargs='*')
    cmdargs = parser.parse_args()

    tool = cmdargs.tool
    toolargs = cmdargs.toolargs

    args = RunArguments(
        split_cwd_tail = cmdargs.split_cwd_tail,
        cwd_base = cmdargs.cwd_base,
        tool_version = cmdargs.tool_version if cmdargs.tool_version else tools[tool].default_version,
        interactive = not cmdargs.non_interactive
    )

    return tool, cmdargs.write_script, args, toolargs
