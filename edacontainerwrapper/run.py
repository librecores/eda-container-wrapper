import sys
import subprocess
import os

from .tools import tools

def split_path(path, depth):
    base = path
    tail = ""
    for d in range(depth):
        base, t = os.path.split(base)
        tail = os.path.join(t, tail)
    return (base, tail)

def run(toolname, args, toolargs):
    tool = tools[toolname]
    version = args.tool_version

    print(f"args.cwd_base: {args.cwd_base}")

    root, tail = split_path(os.getcwd(), args.split_cwd_tail)
    workdir = os.path.join(tool.projectpath, tail)

    cmd = ["docker", "run", "-ti" if args.interactive else "",
            "-v", f"{root}:{tool.projectpath}",
            "-u", f"{os.getuid()}:{os.getgid()}",
            "-w", f"{workdir}",
            f"{tool.image}:{version}"
            ] + toolargs

    return subprocess.call(" ".join(cmd), shell=True)
