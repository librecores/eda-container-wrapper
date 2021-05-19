# EDA Container Wrapper

EDA container wrapper is a work-in-progress generic wrapper tool around open
source EDA tools. The tools are executed in Docker containers and this tool
wraps this execution and keeps an inventory of tools.

It supports three use cases:

1. Run `eda-container-wrapper` to execute the wrapper with given parameters
2. Let `eda-container-wrapper` create a wrapper script (in an executable path for example) with pre-defined settings
3. Run tools from python using the `edacontainerwrapper` module

The settings can be set in the following way in precedence order:

1. As parameters to the `eda-container-wrapper` tool or to the respective functions of `edacontainerwrapper`
2. As environment variables
3. As default settings in the wrapper scripts

## Installation

```shell
$ pip3 install eda-container-wrapper
```

## Supported settings

### Tool version (`--tool-version` or `ECW_TOOL_VERSION`, default: depends on tool)

Sets the version of the tool to use.

### Interactive (`--non-interactive` or `ÈCW_INTERACTIVE`, default: interactive)

Runs the Docker container in interactive mode (allowing to terminate it easily
for example) with the Docker `-ti` flags. Some non-interactive environments such
as CI don't support that (missing tty). Note the difference in logic, the
default is interactive mode which is disabled with the `--non-interactive`
switch. `ECW_INTERACTIVE` keeps it interactive when set to `true` or `1` and it
will be non-interactive otherwise.

### Current work directory base (`--cwd-base` or `ECW_CWD_BASE`, default: not set)

If not empty this is a colon-separated pair of a leading path of the cwd where
the tool was called from and a replacement for this path. This is in particular
useful when called from inside a Docker container, such as in CI. The syntax is:
`<actual path>:<cwd path>`.

### Split the current working directory (`--split-cwd-tail` or `ECW_SPLIT_CWD_TAIL`, default: `0`)

When mapping the current working directory, this setting actually maps the path
up the hierarchy by the given value. This is in particular useful when you need
to access data relative to the current working directory that is in upper and
sibbling folders.

For example, when started from the following folder:

```
CWD=/path/to/my/project/build
```

Setting `--split-cwd-tail=1` the split is into `/path/to/my/project` and
`build`. Each tool has a "project path" that is the volume where the tool is
executed in then by setting the working directory. For a tool with the project
path `/project` it will then mount `/path/to/my/project` to `/project` and the
workdir will be `/project/build`.

This split is executed after processing the `cwd base`.

## Running a Tool

As described above there are different ways to run a tool, that are described in
the following.

### Run `eda-container-wrapper`

The program is called with the parameters as described and the toolname.
Following a `--` parameters to the tool can be supplied.

Example:

```shell
$ eda-container-wrapper verilator -- --version
```

### Create wrapper

To create a `verilator` script that by default executes version 4.100:

```shell
$ eda-container-wrapper --write-script=/usr/local/bin/verilator --tool-version 4.100 verilator
```

and then execute it:

```shell
$ verilator --version
Verilator 4.100 2020-09-07 rev v4.100
```

Setting the environment setting `ECW_TOOL_VERSION` changes the defualt behavior:

```shell
$ ECW_TOOL_VERSION=4.102 verilator --version
Verilator 4.102 2020-10-15 rev v4.102
```

It can be useful to create the script in your virtual environment:

```shell
$ eda-container-wrapper --write-script=$VIRTUAL_ENV/verilator --tool-version 4.100 verilator
```
