#!/usr/bin/python

from importlib.metadata import version
import argparse

description = """
Treerun is a CLI for running teriminal commands from all subdirectories in an
existing tree structure.

The purpose of this software is to be able to run terminal commands from sub-
directories in a tree structure. Each node (sub-directory) must contain the
same subdirectories as its neighbour within a level so that the number of
splits is constant over each level.

The input is YAML-based and should contain a `Tree`-block and a `Modes`-block.
The former defines the tree structure of all directories by including sub-
blocks that contain the directories within that level and the latter is used to
the define available commands (use --example to see an example).
"""

example_tree = """Example tree structure:
---
root-dir                    <-- arbitrary root directory
├── input.yaml              <-- input file must be in root-dir
├── dir1
│   ├── subdir1
│   │   ├── subsubdir1
│   │   │   ├── run.sh
│   │   │   └── test-mod    <-- mod is whatever follows the --modifier flag
│   │   │       └── run.sh
│   │   ├── subsubdir2
│   │   │   ├── run.sh
│   │   │   └── test-mod
│   │   │       └── run.sh
│   │   └── subsubdir3
│   │       ├── run.sh
│   │       └── test-mod
│   │           └── run.sh
│   └── subdir2
│       ├── subsubdir1
│       │   ├── run.sh
│       │   └── test-mod
│       │       └── run.sh
│       ├── subsubdir2
│       │   ├── run.sh
│       │   └── test-mod
│       │       └── run.sh
│       └── subsubdir3
│           ├── run.sh
│           └── test-mod
│               └── run.sh
└── dir2
    ├── subdir1
    │   ├── subsubdir1
    │   │   ├── run.sh
    │   │   └── test-mod
    │   │       └── run.sh
    │   ├── subsubdir2
    │   │   ├── run.sh
    │   │   └── test-mod
    │   │       └── run.sh
    │   └── subsubdir3
    │       ├── run.sh
    │       └── test-mod
    │           └── run.sh
    └── subdir2
        ├── subsubdir1
        │   ├── run.sh
        │   └── test-mod
        │       └── run.sh
        ├── subsubdir2
        │   ├── run.sh
        │   └── test-mod
        │       └── run.sh
        └── subsubdir3
            ├── run.sh
            └── test-mod
                └── run.sh
---
and its associated input:
---
Tree:
  First directory level:   <-- arbitrary name (shown during selection)
    - dir1                 <-- directories must be preceded by dashes
    - dir2
  Second directory level:
    - subdir1              <-- each dir above contains all these
    - subdir2
  Third directory level:
    - subsubdir1           <-- each dir above contains all these
    - subsubdir2
    - subsubdir2

Modes:
  Mode 1:                  <-- name of mode (shown during selection)
    cmd: ./run.sh          <-- command to be run ('command: ' is equally valid)
  Mode 2: 
    cmd: ./run.sh
    dir: test-{mod}        <-- subdir under subsubdir* where {mod} is replaced
---                            by whatever follows the --modifier (or -m) flag
"""

epilog = """Run:
> trn --plant -i input.yaml
to create a tree structure as defined in the input file.

Run:
> trn --example
to see an example tree structure along with what its associated input file 
should look like.
"""


# 80-23=57 spaces wide

version_help = f'\
treerun ver. {version("treerun")}'

plant_help = """attempts to plant a tree as defined in the input YAML-
file
"""

modifier_help = """modifiers are used to substitute {mod} in the \'Modes\' 
block of the input YAML-file
"""

input_help = """input file (YAML-format) that contains a \'Tree\'-block
with the names of all directories in each level and a
\'Modes\'-block that contains all commands (defaults to
tree.yaml in the working directory)
"""

exclude_help = """the program will exclude all nodes corresponding to any 
dir-name given here
"""

all_help = """automatically selects all non-excluded paths without any
prompts
"""

log_help = """information about which programs were run and which 
were not will be stored in a log file with the name
given here
"""

codes_help = """legend for exit codes
"""

example_help = """prints a possible tree structure and the contents of an
associated input file
"""




def argument_parser():
    parser = argparse.ArgumentParser(
        prog='trn',
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    info = parser.add_argument_group(
        'info',
    )
    parser.add_argument(
        '-p', '--plant', action='store_true',
        help=plant_help,
    )
    parser.add_argument(
        '-i', '--input', default='tree.yaml',
        help=input_help,
    )
    parser.add_argument(
        '-m', '--modifier', type=str, 
        help=modifier_help,
    )
    parser.add_argument(
        '-a', '--all', action='store_true',
        help=all_help,
    )
    parser.add_argument(
        '-o', '--output', default=None,
        help=log_help,
    )
    parser.add_argument(
        '-e', '--excluded', nargs='+', default=[],
        help=exclude_help,
    )
    info.add_argument(
        '--version', action='version',
        version=version_help,
    )
    info.add_argument(
        '--example', action='store_true',
        help=example_help,
    )
    info.add_argument(
        '--codes', action='store_true',
        help=codes_help,
    )
    
    return parser.parse_args()
