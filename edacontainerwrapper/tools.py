from collections import namedtuple

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
