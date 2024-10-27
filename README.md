# treerun
CLI for running teriminal commands from all sub-directories in a tree structure.

The purpose of this software is to be able to run terminal commands from sub-directories in a tree structure. Each node (sub-directory) must contain the same sub-directories as its neighbour within a level so that the number of splits is constant over each level.

The config is YAML-based and should contain a `Tree`-block and a `Modes`-block. The former defines the tree structure of all directories by including sub-blocks that contain the directories within that level and the latter is used to the define available commands.

The input is YAML-based and should contain a `Tree`-block and a `Modes`-block. The former specifies the tree structure of all directories and the latter the type of commands, and from which sub-directories of the end-nodes (if there are any), the commands should be run. The program also supports placeholders for certain variables (currently only seed and mode).

Config file example:
```
Tree:
  First directory level:  <-- config file should be in same dir as these
    - dir1
    - dir2
  Second directory level: <-- each dir above contains all these
    - subdir1
    - subdir2
  Third directory level:  <-- each dir above contains all these
    - subsubdir1
    - subsubdir2
    - subsubdir2

Modes:
  Mode 1:                 <-- name of mode (shown during selection)
    cmd: ./run.sh         <-- command to be run ('command: ' is equally valid)
  Mode 2: 
    cmd: ./run.sh
    dir: test-{mod}       <-- subdir under subsubdir*
```
After having placed a file ('input.yaml', for example) containing the above definitions in the same directory as 'dir1' and 'dir2', the program is run by calling:
```
python3 treerun.py --modifier 1 --config input.yaml --log test.log
```

The following is an example where 'dir1', 'subdir1', 'subsubdir1', and 'Mode 1' was selected:
```
————————————————————————————————————————————————————————————————————————————————
First directory level
————————————————————————————————————————————————————————————————————————————————
(1) dir1
(2) dir2
Enter an integer to select an option (press enter to select all): 1
————————————————————————————————————————————————————————————————————————————————
Second directory level
————————————————————————————————————————————————————————————————————————————————
(1) subdir1
(2) subdir2
Enter an integer to select an option (press enter to select all): 1
————————————————————————————————————————————————————————————————————————————————
Third directory level
————————————————————————————————————————————————————————————————————————————————
(1) subsubdir1
(2) subsubdir2
(3) subsubdir3
Enter an integer to select an option (press enter to select all): 1
————————————————————————————————————————————————————————————————————————————————
Select mode:
————————————————————————————————————————————————————————————————————————————————
(1) Mode 1
(2) Mode 2
Select an option: 1
————————————————————————————————————————————————————————————————————————————————
Summary:
————————————————————————————————————————————————————————————————————————————————
Mode:              Mode 1
System             ['dir1']
Parameter set 1    ['subdir1']
Parameter set 2    ['subsubdir1']
————————————————————————————————————————————————————————————————————————————————
Checking directories:
————————————————————————————————————————————————————————————————————————————————
All relevant directories exist. Proceeding with submission attempt.
————————————————————————————————————————————————————————————————————————————————
Submitting:
————————————————————————————————————————————————————————————————————————————————
Moving to:    /dir1/subdir1/subsubdir1
Running:      ./run.sh
```
which produced the following output to the file 'test.log':
```
————————————————————————————————————————————————————————————————————————————————
Mode:         Mode 1
Submitted:    2024-10-26 13:07:48.465873
Root dir:     /home/user/Documents/python/treerun/v0.0.1/test

Successfully submitted:
/dir1/subdir1/subsubdir1    ./run.sh
```
and after running with the flag `--modifier SOME_MODIFIER` and selecting mode nr 2, the log file contains
```
————————————————————————————————————————————————————————————————————————————————
Mode:         Mode 1
Submitted:    2024-10-26 13:07:48.465873
Root dir:     /home/user/Documents/python/treerun/v0.0.1/test

Successfully submitted:
/dir1/subdir1/subsubdir1    ./run.sh
————————————————————————————————————————————————————————————————————————————————
Mode:         Mode 2
Submitted:    2024-10-26 14:36:38.812880
Root dir:     /home/user/Documents/python/treerun/v0.0.1/test

Successfully submitted:
/dir1/subdir1/subsubdir1/test-SOME_MODIFIER    ./run.sh
```

