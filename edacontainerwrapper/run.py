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

    cwd = os.getcwd()
    print(f"CWD in runner: {cwd}")
    if args.cwd_base:
        replace, base = args.cwd_base.split(":")
        if cwd.startswith(base):
            print(f" replace {base} with {replace}")
            cwd = os.path.join(replace,cwd[len(base):].lstrip("/"))
            print(f"CWD: {cwd}")

    root, tail = split_path(cwd, args.split_cwd_tail)
    print(f"split root '{root}' and tail '{tail}'")
    workdir = os.path.join(tool.projectpath, tail)
    print(f"CWD in container: {workdir}")

    cmd = ["docker", "run", "-ti" if args.interactive else "",
            "-v", f"{root}:{tool.projectpath}",
            "-u", f"{os.getuid()}:{os.getgid()}",
            "-w", f"{workdir}",
            f"{tool.image}:{version}"
            ] + toolargs

    print(cmd)

    return subprocess.call(" ".join(cmd), shell=True)
