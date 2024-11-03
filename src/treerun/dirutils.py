#!/usr/bin/python

import os
import sys
import itertools
import functools

from treerun import broadcast
import treerun.main as trm

"""Methods for obtaining, pruning/grafting and checking the existence of
paths."""

def graft_paths(paths:list, graft_point:str) -> list:
    """Given a list of paths, returns a list of paths grafted and grafted 
    with a new path specified as a mode dir in the input.

    In practise this is used to run commands from non-endpoint nodes.

    Keyword arguments:
      paths:        list of paths to be grafted, if possible
      graft_point:  point of entry for grafting where the string section 
                    before the first '/' is part of one of the given paths
    """
    grafted_paths = []      
    entry_point = graft_point[1:].split('/')[0]
    for path in paths:
        if (len(graft_point) > 0) and (entry_point in path.split('/')):
            grafted_path = path.partition(entry_point)[0]+graft_point[1:]
            if grafted_path not in grafted_paths:
                grafted_paths.append(grafted_path)
    
    return grafted_paths


def check_files(paths:list, root_dir:str=None) -> tuple:
    """Given a list of paths, returns the lists of the paths that does, and
    does not, exist on the drive.

    Keyword argument:
      paths:  list of paths
    """
    found, not_found = [], []
    
    # Determine which directories does and does not exist
    for path in paths:
        if os.path.isdir(root_dir+path):
            found.append(path)
        else:
            not_found.append(path)

    # Make sure user wants to continue if missing files
    broadcast.header(f'Checking directories:')

    ## None of the directories were found: exit
    if len(found) == 0:
        print('Could not locate the relevant directories.')
        print('\nPlease make sure that the appropriate directories exist and that all modifiers')
        print('in the YAML input (if any) have been supplied.')
        trm.ExitCode(2)

    ## Some directories were not found, still continue?
    elif len(not_found) > 0:
        print('Unable to locate the following directories:')
        for file in not_found:
            print(file)

        try:
            q = input('Do you still want to continue (y/[n])? ').lower()
            if q not in ['y', 'yes']:
                print('Closing.')
                sys.exit()
        except:
            trm.ExitCode(0)

    # All directories were found
    elif (len(found) == len(paths)) and (len(not_found) == 0):
        print('All relevant directories exist.')
        print('\nProceeding with submission attempt.')

    return (found, not_found)


def get_paths(paths:dict) -> list:
    """Returns a list of paths genereted from Cartesian products of the 
    values in a given dictionary.

    Keyword arguments:
      paths: non-nested dictionary will treat values as being of type 'list'
    """
    prod = itertools.product(*paths.values())
    paths = list(map(lambda e: '/'+'/'.join(e), prod))
    return paths