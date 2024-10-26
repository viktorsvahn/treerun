#!/usr/bin/python

import sys
import os
import argparse
import json
import yaml
import subprocess
import copy
import datetime
from pathlib import Path
#import numpy as np

import itertools
import functools
import collections


"""
This should be reconstructed to use lists since the indices in dict form within
the YAML-file is superfluous!
"""

# Add argparse command to ignore keywords, such as for example MULTIHEAD
parser = argparse.ArgumentParser(
    prog='ProgramName',
    description='What the program does',
    epilog='Text at the bottom of help')
parser.add_argument('-m', '--modifier')
parser.add_argument('-c', '--config', default='input.yaml')
parser.add_argument('-i', '--ignore', nargs='+', default=[])
parser.add_argument('-l', '--log', default=None)
args = parser.parse_args()


# This should be the name of the test dir
#test_dir = 'test_run-'


def whitespace(strings, tab_width=4, max_length=None):
    """Returns a dictionary with the same keys as the original dictionary but
    with a number of spaces as values instead.

    The number of spaces corresponds to the difference between all keys and the
    longest key (+tab_width).
    """
    if type(strings) == list:
        lengths = [len(string) for s in strings]
        if max_length == None:
            longest_string = max(lengths)
        else:
            longest_string = max_length+tab_width
        spaces = {string:(longest_string-length) for string, length in zip(strings, lengths)}

    elif type(strings) == dict:
        # Get longest name
        name_lengths = {key:len(key) for key in strings}
        if max_length == None:
            longest_string = name_lengths[max(name_lengths, key=name_lengths.get)]+tab_width
        else:
            longest_string = max_length+tab_width

        # Create whitespace map
        spaces = {key:(longest_string-val)*' ' for key,val in name_lengths.items()}

    return spaces, longest_string


def tabulate(data, max_length=None):
    assert type(data)==dict, ValueError('The \'tabulate\' function takes a dictionary as input.')
    space, _ = whitespace(data, max_length=max_length)
    for key,val in data.items():
        print(f'{key}{space[key]}{val}')


def convert_placeholders(dictionary, args):
    """Returns a copy of the dictionary where placeholders have been replaced
    by the variables defined in 'args'.

    Placeholders in the YAML-file are defined as {arg} where 'arg' will be 
    replaced by its corresponding mapping defined by 'args'

    Keyword arguments:
      dictionary:  dictionary subject to placeholder conversion
      args:        dictionary with proper placeholder-variable map, e.g,
                   args = dict(mod=modifier, mode=mode, ...)
    """
    tmp = copy.deepcopy(dictionary)

    # Attempt conversion based on type
    for key,val in dictionary.items():
        if type(val) == list:
            for i,v in enumerate(val):
                # Convert if subelement is string
                if type(v) == str:
                    tmp[key][i] = v.format(**args)

        elif type(val) == dict:
            for k,v in val.items():
                # Convert if subelement is string
                if type(v) == str:
                    tmp[key][k] = v.format(**args)

        # Convert if subelement is string
        elif type(val) == str:
            tmp[key] = val.format(**args)

    return tmp


def level_cycler(description, options):
    while True:
        # Attempt selection
        index_selection = input(description)

        # Evaluate selection, repeat attempt if criteria not met
        ## Single entry selections are simple index-slices of a list
        if index_selection.isdigit():
            index_selection = int(index_selection)

            ## Make sure index is valid
            if 1 <= index_selection < len(options)+1:
                if type(options) == list:
                    selection = options[index_selection-1]
                
                # Do not quite understand why this is needed
                elif type(options) == dict:
                    selection = options[index_selection]

                # Keep only non-ignored selections
                if selection not in args.ignore:
                    break
                else:
                    print('This option is being ignored. Please select another.')
            else:
                print(f'Integer selections must be between 1 and {len(options)}')
            continue

        # If selection is not digit, select all using '*' or simply 'enter'
        elif (index_selection == '') and (type(options) != dict):
            # Filter all ignored if multiple selections
            selection = [s for s in options if s not in args.ignore]
            break
        elif type(options) == dict:
            print(f'Please specify a single mode.')
        else:
            print(f'Enter an integer or press enter to select all.')
        continue

    return selection


def level_select(dictionary, ignore):
    choices = {}
    integer_to_mode_map = {}
    for key,val in dictionary.items():
        # Show options available for selection
        header(key)
        if type(val) == list:
            for i, v in enumerate(val):
                if v in ignore:
                    print(f'({i+1}) {v} (will be ignored)')
                else:
                    print(f'({i+1}) {v}')

            # Make selection
            selection = level_cycler('Enter an integer to select an option (press enter to select all): ', val)

            # Selection must be a list (preparation for cartiesian product)
            if type(selection) == str:
                choices[key] = [selection]
            else:
                choices[key] = selection

    return choices


def header(string):
    """Simple header with em-dash (U+2014).
    """
    print(80*'\u2014')
    print(string)
    print(80*'\u2014')


def mode_select(dictionary, modifier):
    integer_to_mode_map = {}

    # Select mode
    header('Select mode:')
    for i, (key,val) in enumerate(dictionary.items()):
        print(f'({i+1}) {key}')
        integer_to_mode_map[i+1] = key,val
    selection = level_cycler('Select an option: ', integer_to_mode_map)
    #print(selection)

    # Summarise and print selections. Could be prettier...
    indentation, longest_path_name = whitespace(choices)
    header('Summary:')
    tmp = {
        'Mode:':selection[0],
        'Modifier:':modifier,
    }
    tabulate(tmp|choices)

    return selection


def get_paths(dictionary):
    prod = itertools.product(*dictionary.values())
    paths = list(map(lambda e: '/'+'/'.join(e), prod))
    return paths


def check_files(paths):
    # Determine which files exist
    cwd = os.path.dirname(__file__)
    is_dir = lambda p: os.path.isdir(p)
    found, not_found = [], []
    for path in paths:
        if is_dir(cwd+path):
            found.append(path)
        else:
            not_found.append(path)

    # Make sure user wants to continue if missing files
    header(f'Checking directories:')
    if len(found) == 0:
        print('Could not locate the relevant directories.')
        print('\nPlease make sure that the appropriate directories exist and that all modifiers\nin the YAML input (if any) have been supplied.')
        quit()
    elif len(not_found) > 0:
        print('Unable to locate the following directories:')
        for file in not_found:
            print(file)
        if input('Do you still want to continue (y/[n])? ').lower() not in ['y', 'yes']:
            print('Closing.')
            quit()
    elif (len(found) == len(paths)) and (len(not_found) == 0):
        print('All relevant directories exist. Proceeding with submission attempt.')

    return found, not_found


def run(mode, dictionary, modifier, log_file):
    mode, mode_dict = mode

    
    # Convert placeholders to variables
    placeholder_map = dict(
        mod=modifier,
        mode=mode
    )
    mode_dict = convert_placeholders(mode_dict, placeholder_map)
    
    # Path to script
    cwd = os.path.dirname(__file__)

    # Stores attempts for logging purposes
    successful, unsuccessful = [],[]

    # Get command
    try:
        cmd = mode_dict['cmd']
    except:
        try:
            cmd = mode_dict['command']
        except:
            raise KeyError('The current mode does not seem to have any associated command.')

    # Get sub-dir to run in, if speecified
    try:
        run_dir = '/'+mode_dict['dir']
    except:
        try:
            run_dir = '/'+mode_dict['directory']
        except:
            run_dir = ''


    # Get paths
    paths = [f'{p}{run_dir}' for p in get_paths(dictionary)]
    #sprint(run_dir)

    # Make sure the paths exist, then submit those that do
    found, not_found = check_files(paths)

    # Attempt to submit all files that were found
    header(f'Submitting:')
    for path in found:
        # Attempt to run
        try:
            os.chdir(f'{cwd}/{path}')
            tabulate(
                {
                    'Moving to:':path,
                    'Running:':cmd,
                }
            )
            #print(f'Moved to: {path}')
            #print(f'Running: {cmd}')
            subprocess.call(cmd, shell=True)
            successful.append(path)
        except FileNotFoundError as e:
            print(e)
            print('Proceding to next file.')
            unsuccessful.append(path)

    # Lengths of all paths, used for even tabulating
    lengths = [len(string) for string in found+not_found+unsuccessful]

    # Logging
    if log_file != None:
        with open(f'{cwd}/{log_file}', 'a') as sys.stdout:
            print(80*'\u2014')
            tabulate(
                {
                    'Mode:':mode,
                    'Submitted:':datetime.datetime.now(),
                    'Root dir:':cwd,
                }
            )
            print()
            print('Successfully submitted:')
            tabulate({p:cmd for p in successful}, max(lengths))

            if len(unsuccessful) > 0:
                print()
                print('Unsuccessful submissions:')
                tabulate({p:cmd for p in unsuccessful})

            if len(not_found) > 0:
                print()
                print('Not found:')
                tabulate({p:cmd for p in not_found})




if __name__ == '__main__':
    if args.ignore != []:
        print(f'Ignoring: {args.ignore}')

    # Path to this script
    cwd = os.path.dirname(__file__)

    # Obtain levels and modes
    input_path = f'{cwd}/{args.config}'
    if os.path.isfile(input_path):
        with open(input_path, 'r') as f:
            data = yaml.safe_load(f)
        levels = data['Tree']
        modes = data['Modes']
        #modes = convert_placeholders(data['Modes'])
    else:
        raise FileNotFoundError('Please make sure there is a proper config file (YAML) in the script directory.')


    # Select levels
    choices = level_select(levels, args.ignore)

    # Select modes and run
    mode = mode_select(modes, args.modifier)
    #quit()
    run(mode, choices, args.modifier, log_file=args.log)


