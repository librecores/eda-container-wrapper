import sys
import subprocess
from collections import namedtuple
import os

RunArguments = namedtuple("RunArguments", "split_cwd_tail tool_version interactive")
RunArgumentsDefaults = RunArguments(split_cwd_tail=0, tool_version=None, interactive=True)

def split_path(path, depth):
    base = path
    tail = ""
    for d in range(depth):
        base, t = os.path.split(base)
        tail = os.path.join(t, tail)
    return (base, tail)

ToolContainer = namedtuple("Toolcontainer", "image projectpath default_version")

tools = {
    "verilator": ToolContainer(
        image="verilator/verilator",
        projectpath="/work",
        default_version="latest"),
    "openlane": ToolContainer(
        image="edalize/openlane-sky130",
        projectpath="/project",
        default_version="v0.12")
}

def run(toolname, args, toolargs):
    if toolname not in tools:
        raise RuntimeError(f"Unknown Tool: {toolname}")

    tool = tools[toolname]

    version = os.getenv("TOOL_VERSION", args.tool_version)

    root, tail = split_path(os.getcwd(), int(os.getenv("SPLIT_CWD_TAIL", args.split_cwd_tail)))
    workdir = os.path.join(tool.projectpath, tail)

    cmd = ["docker", "run", "-ti" if args.interactive else "",
            "-v", f"{root}:{tool.projectpath}",
            "-u", f"{os.getuid()}:{os.getgid()}",
            "-w", f"{workdir}",
            f"{tool.image}:{version}"
            ] + toolargs

    return subprocess.call(" ".join(cmd), shell=True)
