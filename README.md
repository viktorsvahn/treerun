# treerun
CLI for running teriminal commands from all subdirectories in a tree structure.

This software is used for running terminal/bash commands from subdirectories in a tree of direcotries. Each node (sub-directory) must contain the same sub-direcotries as its neighbour. That is, the number of splits must be constant for each level.

The input is YAML-based and should contain a `Tree`-block and a `Modes`-block. The former specifies the tree structure of all directories and the latter the type of commands, and from which sub-directories of the end-nodes (if there are any), the commands should be run. The program also supports placeholders for certain variables (currently only seed and mode).

# Example:
We consider a tree structure with three levels, the first two levels each have two directories (system1 and system2 each contain param11 and param12.) The third and last level contains three directories (param21, param22, param23), resulting in a total of 12 end nodes that each contain some mode for running. In the below example 'Training' and 'Analysis' are the two available modes. Selecting 'Training' will attempt to run the command './run.sh' under all twelve paths with the pattern '/\*/\*/param2\*'. On the hand, selecting 'Analysis' will result a script with the same name being run from '/\*/\*/param2\*/test-{seed}' where 'mod' will be exchanged for a modifier given when running the program (optional).
```
Tree:
  System:
    - system1
    - system2
  Parameter set 1:
    - param11
    - param12
  Parameter set 2:
    - param21
    - param22
    - param23

Modes:
  Training: 
    cmd: ./run.sh
  Analysis: 
    cmd: ./run.sh
    dir: test-{mod}
```
After having placed a file ('input.yaml', for example) containing the above definitions in the same directory as 'system1' and 'system2', the program is run by calling:
```
python3 treerun.py --modifier 1 --config input.yaml --log test.log
```

The following is an example where 'system1', 'param11', 'param21', and 'Training' was selected:
```
————————————————————————————————————————————————————————————————————————————————
System
————————————————————————————————————————————————————————————————————————————————
(1) system1
(2) system2
Enter an integer to select an option (press enter to select all): 1
————————————————————————————————————————————————————————————————————————————————
Parameter set 1
————————————————————————————————————————————————————————————————————————————————
(1) param11
(2) param12
Enter an integer to select an option (press enter to select all): 1
————————————————————————————————————————————————————————————————————————————————
Parameter set 2
————————————————————————————————————————————————————————————————————————————————
(1) param21
(2) param22
(3) param23
Enter an integer to select an option (press enter to select all): 1
————————————————————————————————————————————————————————————————————————————————
Select mode:
————————————————————————————————————————————————————————————————————————————————
(1) Training
(2) Analysis
Select an option: 1
————————————————————————————————————————————————————————————————————————————————
Summary:
————————————————————————————————————————————————————————————————————————————————
Mode:              Training
System             ['system1']
Parameter set 1    ['param11']
Parameter set 2    ['param21']
————————————————————————————————————————————————————————————————————————————————
Checking directories:
————————————————————————————————————————————————————————————————————————————————
All relevant directories exist. Proceeding with submission attempt.
————————————————————————————————————————————————————————————————————————————————
Submitting:
————————————————————————————————————————————————————————————————————————————————
Moving to:    /system1/param11/param21
Running:      ./run.sh
```
which produced the following output to the file 'test.log':
```
————————————————————————————————————————————————————————————————————————————————
Mode:         Training
Submitted:    2024-10-26 13:07:48.465873
Root dir:     /home/user/Documents/python/treerun/v0.0.1/test

Successfully submitted:
/system1/param11/param21    ./run.sh
```
and after running with the flag `--modifier SOME_MODIFIER` and selecting mode nr 2, the log file contains
```
————————————————————————————————————————————————————————————————————————————————
Mode:         Training
Submitted:    2024-10-26 13:07:48.465873
Root dir:     /home/user/Documents/python/treerun/v0.0.1/test

Successfully submitted:
/system1/param11/param21    ./run.sh
————————————————————————————————————————————————————————————————————————————————
Mode:         Analysis
Submitted:    2024-10-26 14:36:38.812880
Root dir:     /home/user/Documents/python/treerun/v0.0.1/test

Successfully submitted:
/system1/param11/param21/test-SOME_MODIFIER    ./run.sh
```

