#!/usr/bin/python

import os
import sys
import yaml
import copy
import datetime
import subprocess
import itertools
import functools
from importlib.metadata import version
import argparse

from treerun import broadcast
from treerun import dirutils
from treerun import YAMLutils
from treerun.parser import argument_parser

args = argument_parser()


class ExitCode:
    """Exit codes used for graceful shutdowns of the program.

    Class attributes:
      legend:  short description of exit codes
    """
    legend = {
        0:'A problem occurred during input-selection',
        1:'Missing YAML-input',
        2:'The necessary files could not be found',
        3:'Error converting placeholders',
        4:'Missing mode-command',
        5:'Log-file does not exist',
    }
    def __init__(self, exit_code=None,loc=''):
        self.exit_code = exit_code
        if self.exit_code != None:
            print(f'exit code: {self.exit_code}')
            sys.exit()


class Tree:
    """A class used to run shell commands from different locations on the disk.

    Attributes:
      yaml_data:         contains the full contents of the input YAML file
      modifier:          replaces {mod} in the YAML file
      excluded:          nodes that are being excluded from selection
      select_all:        select all nodes of the tree
      log_file:          name of log file
      tree:              tree-structure defined in the input
      modes:             run-modes defined in the input
      root_dir:          root-dir that contains the tree structure
      succesful:         paths of succesful runs
      unsuccesful:       paths of unsuccesful runs

    Methods:
      plant:             not yet implemented
      selection_prompt:  prompts the user to select a node or a run-mode
      select:            used to select nodes and modes during operation
      logger:            logs the outcome to a file
      climb:             runs the selected mode at the selected nodes
    """
    def __init__(self, yaml_data:str, modifier:str, excluded:list, select_all:bool, log_file:str) -> None:
        if yaml_data is None: self.plant
        else: self.yaml_data = YAMLutils.load_input(yaml_data)
        self.modifier = modifier
        self.excluded = excluded
        self.select_all = select_all
        self.log_file = log_file

        # 'Root: dir' specifies where the tree is. Default is same dir as YAML
        if 'Root' in self.yaml_data: 
            self.root_dir = os.path.abspath(self.yaml_data['Root'])
        else: self.root_dir = os.getcwd()
        #print(self.root_dir) # HERE IS A TEMPORARY PRINT STATEMENT

        # Convert placeholders to variables
        ## Defined in input.yaml
        if 'Handles' in self.yaml_data:
            placeholder_map = self.yaml_data['Handles']
        elif 'Placeholders' in self.yaml_data:
            placeholder_map = self.yaml_data['Placeholders']
        
        else:
            ## Default if not in yaml
            placeholder_map = dict(
                mod=self.modifier,
                #mode=mode,
            )

        # Make sure that cli input overrides anything in config
        if self.modifier is not None:
            placeholder_map['mod'] = self.modifier

        # Define tree and mode options
        self.tree = self.yaml_data['Tree']
        self.modes = YAMLutils.convert_handles(self.yaml_data['Modes'], placeholder_map)
        self.successful, self.unsuccessful = [],[]


    def plant(self, arg):
        """Somehow generate a tree if no input has been given or if directories
        in input do not exist.
        """
        pass


    def selection_prompt(self, description:str, options:dict or list, select_all:bool) -> list:
        """Promts the user to give an enter an input in the form of an integer 
        and returns the options corresponding to it.

        Keyword arguments:
          description:  short description of the type of input that is being 
                        requested
          options:      the allowed options to select from
          select_all:   boolean that automatically selects all options
        """
        if select_all:
            selection = [opt for opt in options if opt not in self.excluded]
        else:            
            while True:
                # Attempt selection
                try:
                    index_selection = input(description)
                except EOFError as e:
                    # This exception is helpful when running the test script
                    print(e)
                    ExitCode(0)

                # Evaluate selection, repeat attempt if criteria not met
                ## Single entry selections are simple index-slices of a list
                if index_selection.isdigit():
                    index_selection = int(index_selection)

                    ## Make sure index is valid
                    if 1 <= index_selection < len(options)+1:
                        if type(options) == list:
                            # Shift of -1 needed for list since prompt starts from 1
                            selection = options[index_selection-1]
                        
                        # Do not quite understand why this is needed
                        elif type(options) == dict:
                            selection = options[index_selection]

                        # Keep only non-excluded selections
                        if selection not in self.excluded:
                            break
                        else:
                            print('This option has been excluded. Please select another.')
                    else:
                        print(f'Integer selections must be between 1 and {len(options)}')
                    continue

                # If selection is not digit, select all using '*' or simply 'enter'
                elif (index_selection in ['', '*']) and (type(options) != dict):
                    # Filter all excluded if multiple selections
                    selection = [s for s in options if s not in self.excluded]
                    break
                elif type(options) == dict:
                    print('Only one mode at a time can be selected.')
                else:
                    print('Enter an integer or press enter to select all.')
                continue

        return selection


    def select(self, selection_type:str) -> dict or list:
        """Selects 'branches' or 'modes' from user input.

        Keyword argument:
          selection_type:  'branches' or 'modes' depending on what is being 
                           selected
        """
        branches = {}
        integer_to_mode_map = {}
        
        # Select branches
        if selection_type == 'branches':
            for key, level in self.tree.items():
                broadcast.header(key)

                # Show options available for selection
                for i, option in enumerate(level):
                    if option in self.excluded:
                        print(f'({i+1}) {option} (excluded)')
                    else:
                        print(f'({i+1}) {option}')

                # Make selection
                desc = 'Enter an integer to select an option (press enter to select all): '
                selection = self.selection_prompt(
                    desc,
                    level,
                    select_all=self.select_all
                )

                # Selection must be a list (preparation for cartiesian product)
                if type(selection) == str:
                    branches[key] = [selection]
                else:
                    branches[key] = selection
            return branches
        
        # Select mode
        elif selection_type == 'mode':
            # Select mode
            broadcast.header('Select mode:')
            for i, (key,option) in enumerate(self.modes.items()):
                print(f'({i+1}) {key}')
                integer_to_mode_map[i+1] = key,option
            mode = self.selection_prompt(
                'Select an option: ',
                integer_to_mode_map,
                select_all=False
            )
            return mode


    def logger(self, log_file, mode, cmd, max_length, found, not_found):
        """Stores the outcome of a run into a log file.

        This method is somewhat clumsy but its purpose is to remove clutter from
        the climb-method.

        Keyword arguments:
          log_file:    the name of the log file
          mode:        the selected mode
          cmd:         the command that was run
          max_length:  longest path length (controls whitespace between columns)
          found:       all paths that were found on the disk
          not_found:   all paths that were not found on the disk
        """
        try:
            with open(f'{self.root_dir}/{log_file}', 'a') as sys.stdout:
                broadcast.horizontal_line()
                broadcast.tabulate(
                    {
                        'Mode:':mode,
                        'Submitted:':datetime.datetime.now(),
                        'Root dir:':self.root_dir,
                    }
                )
                print()
                print('Successfully submitted:')
                broadcast.tabulate({p:cmd for p in self.successful}, max_length)

                if len(self.unsuccessful) > 0:
                    print()
                    print('Unsuccessful submissions:')
                    broadcast.tabulate({p:cmd for p in self.unsuccessful}, max_length)

                if len(not_found) > 0:
                    print()
                    print('Not found:')
                    broadcast.tabulate({p:cmd for p in not_found}, max_length)
        except:
            ExitCode(5)


    def climb(self) -> None:
        """Goes through the tree and runs the selected mode (command) at all the
        selected nodes/leaves/branches.
        """
        # Obtain modes and branches to run from
        branches = self.select('branches')
        selected_mode, mode_params = self.select('mode')

        # Collect arguments form list, if specified
        if 'args' in mode_params:
            cmd_args = ' '+' '.join(mode_params['args'])
        elif 'arguments' in mode_params:
            cmd_args = ' '+' '.join(mode_params['arguments'])
        else:
            cmd_args = ''

        # Get command
        if 'cmd' in mode_params:
            cmd = mode_params['cmd']+cmd_args
        elif 'command' in mode_params:
            cmd = mode_params['command']+cmd_args
        else:
            ExitCode(4)
            raise KeyError('The selected mode has no command.')

        # Get sub-dir to run in, if specified
        if 'dir' in mode_params:
            run_dir = '/'+mode_params['dir']
        elif 'directory' in mode_params:
            run_dir = '/'+mode_params['directory']
        else:
            run_dir = ''

        broadcast.header('Summary:')
        tmp = {
            'Mode:':selected_mode,
            'Command:':cmd,
        }
        if self.modifier is not None:
            tmp['Modifier:'] = self.modifier
        if run_dir != '':
            tmp['Run directory:'] = run_dir
        broadcast.tabulate(tmp|branches)
        
        # Attempts pruning of paths if the specified run_dir has a lower level than 
        # the maximum
        paths = dirutils.get_paths(branches)
        pruned_paths = dirutils.graft_paths(paths, run_dir)

        # Get paths and make find out which actually exist
        if len(pruned_paths) == 0:
            paths = [p+run_dir for p in paths]
            found, not_found = dirutils.check_files(paths, self.root_dir)
        else:
            paths = [p for p in pruned_paths]
            found, not_found = dirutils.check_files(pruned_paths, self.root_dir)

        # RUN
        # Attempt to submit all files that were found
        broadcast.header(f'Submitting:')
        for path in found:
            # Attempt to run
            try:
                os.chdir(self.root_dir+path)
                broadcast.tabulate(
                    {
                        'Moving to:':path,
                        'Running:':cmd,
                    }
                )
                subprocess.call(cmd, shell=True)
                self.successful.append(path)

            # Log unsuccessful attempts
            except FileNotFoundError as e:
                print(e)
                print('Proceding to next file.')
                self.unsuccessful.append(path)

        # Lengths of all paths, used for even tabulating
        max_length = max([len(string) for string in found+not_found+self.unsuccessful])

        # Logging
        if self.log_file is not None:
            self.logger(
                self.log_file,
                selected_mode,
                cmd,
                max_length,
                found,
                not_found
            )

"""
class Dummy:
    def __init__(self,input_file=None,select_all=False,modifier=None,excluded=[], output='test.log'):
        self.input_file = input_file
        self.all = select_all
        self.modifier = modifier
        self.excluded = excluded
        self.output = output
"""


def main():
    #args = Dummy(input_file='list.yaml')
    tree = Tree(
        yaml_data=args.input,
        modifier=args.modifier,
        excluded=args.excluded,
        select_all=args.all,
        log_file=args.output,
    )
    tree.climb()


if __name__ == '__main__':
    main()