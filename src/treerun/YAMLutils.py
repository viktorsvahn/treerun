#!/usr/bin/python

import os
import yaml
import copy

# Import: broadcast, exitcode
#import broadcast
#from main import ExitCode



"""Processor for YAML files dealing with both input, output and conversion
of handles."""

def load_input(yaml_file:str) -> dict:
    """Loads a YAML file."""
    with open(yaml_file, 'r') as f:
        yaml_data = yaml.safe_load(f)
    return yaml_data

def convert_handles(data:dict or str, handle_map:dict) -> dict:
    """Converts placeholders/handles in a data defined a handle map.

    Placeholders in the YAML-file are defined as {arg} where 'arg' will be 
    replaced by its corresponding mapping defined by 'args'

    Keyword arguments:
      data:  data subject to placeholder/handle conversion
      handle_map:  data with proper placeholder-variable maps, e.g,
                   args = dict(arg1=value1, arg2=value2, ...)
    """
    if type(data) == str:
        tmp = data.format(**handle_map)

    else:
        tmp = copy.deepcopy(data)
        # Attempt conversion based on type
        for key,val in data.items():

            if type(val) == list:
                for i,v in enumerate(val):
                    # Convert if subelement is string
                    if type(v) == str:
                        #tmp[key][i] = v.format(**handle_map)
                        try:
                            tmp[key][i] = v.format(**handle_map)
                        except:
                            print(f'Unable to convert handles (in list)')

            elif type(val) == dict:
                for k,v in val.items():
                    # Convert if subelement is string
                    if type(v) == str:
                        #tmp[key][k] = v.format(**handle_map)
                        try:
                            tmp[key][k] = v.format(**handle_map)
                        except:
                            print(f'Unable to convert handles (in dict)')

            # Convert if subelement is string
            elif type(val) == str:
                #tmp[key] = val.format(**handle_map)
                try:
                    tmp[key] = val.format(**handle_map)
                except:
                    print(f'Unable to convert handles (string)')

    return tmp

def yaml_from_paths():
    """Genrerate YAML tree from paths. The tree should be printed and the 
    user can save it manually, or be able to use '>'. It must therefore be a
    command.
    """
    pass

def paths_from_yaml():
    pass
